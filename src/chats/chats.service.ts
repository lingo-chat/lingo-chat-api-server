import { BadRequestException, Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { ChatRoom } from './entities/chatRoom.entity';
import { Repository, DataSource } from 'typeorm';
import { WebsocketClientGateway } from 'src/websocket-client/websocket-client.gateway';
import { PersonaService } from 'src/persona/persona.service';
import { UsersService } from 'src/users/users.service';
import { personaList } from 'src/persona/entities/personaList.entity';
import { User } from 'src/users/entities/user.entity';
import { SaveRedisLogsDto } from './dtos/save-redis-logs.dto';
import { ChatLog } from './entities/chatLog.entity';
import { ModelAnswer } from './entities/modelAnswer.entity';
import { ChatsExeption } from './classes/chats.exception.message';
import { RedisCacheService } from 'src/redis/redis-cache.service';

@Injectable()
export class ChatsService {
	constructor(
		private readonly personaService: PersonaService,
		private readonly usersService: UsersService,
		private readonly websocketClientGateway: WebsocketClientGateway,
		@InjectRepository(ChatRoom)
		private readonly chatRoomRepository: Repository<ChatRoom>,
		@InjectRepository(ChatLog)
		private readonly chatLogRepository: Repository<ChatLog>,
		@InjectRepository(ModelAnswer)
		private readonly modelAnswerRepository: Repository<ModelAnswer>,
		private readonly redisCacheService: RedisCacheService,
		private readonly dataSource: DataSource,
	) {}

	async processFistChatMessage(provideId: string, message: string, personaId: number) {
		const persona = await this.personaService.getPersona(personaId);
		const personaName = persona.name;

		const title = await this.createChatTitle(message, personaName);
		const chatRoom = await this.createChatRoom(provideId, title, persona);
		const newChatRoom = await this.findNewChatRoom(chatRoom.id);

		this.websocketClientGateway.sendNewChatRoom('created_new_chat_room', {
			userId: provideId,
			newChatRoom,
		});

		const str = JSON.stringify({
			user_id: provideId,
			chat_room_id: chatRoom.id,
			user_message: message,
		});

		await this.redisCacheService.pushQueue('user_ms_queue', str);

		return {
			chatRoomId: chatRoom.id,
			title: chatRoom.title,
		};
	}

	private async createChatTitle(message: string, personaName: string) {
		const truncatedMessage = message.substring(0, 10);
		return personaName + `-` + truncatedMessage;
	}

	private async createChatRoom(provideId: string, title: string, persona: personaList) {
		const user = await this.usersService.findUser({ provide_id: provideId });

		const newChatRoom = {
			title: title,
			user: user,
			persona: persona,
		};

		return await this.chatRoomRepository.save(newChatRoom);
	}

	async findChatRooms(user: User) {
		const chatRooms = await this.chatRoomRepository.find({
			where: {
				user: { id: user.id },
			},
			relations: ['persona'],
		});

		return chatRooms;
	}

	async findNewChatRoom(chatRoomId: number) {
		const newChatRoom = await this.chatRoomRepository.findOne({
			where: { id: chatRoomId },
			relations: ['persona'],
		});

		return newChatRoom;
	}

	async getRedisLogs(chatRoomId: string) {
		const chatLogs = await this.redisCacheService.getList(chatRoomId);
		console.log(chatLogs);
		return chatLogs;
	}

	async createDBLogList(chatLogs: ChatLog[], modelAnswers: ModelAnswer[], userId: string, chatRoomId: number) {
		const logList = [];
		for (let i = 0; i < chatLogs.length; i++) {
			// ChatLog 데이터를 먼저 추가
			logList.push({
				role: 'user',
				content: chatLogs[i].question,
				user_id: userId,
				chat_room_id: chatRoomId,
			});

			if (modelAnswers[i]) {
				logList.push({
					role: 'assistant',
					content: modelAnswers[i].answer,
					user_id: userId,
					chat_room_id: chatRoomId,
					created_time: modelAnswers[i].response_time,
				});
			}
		}

		return logList;
	}

	async getDBLogs(chatRoomId: string, user?: User) {
		const userId = user?.provide_id ?? null;
		const chatRoom = await this.findNewChatRoom(Number(chatRoomId));

		// 나중에 함수 분리하기
		const chatLogs = await this.chatLogRepository.find({
			where: {
				chat_room: { id: chatRoom.id },
			},
		});

		const modelAnswers = [];
		for (const log of chatLogs) {
			const answer = await this.modelAnswerRepository.find({
				where: {
					chatLog: { id: log.id },
				},
			});

			modelAnswers.push(answer[0]);
		}

		return await this.createDBLogList(chatLogs, modelAnswers, userId, Number(chatRoomId));
	}

	async saveChatLogs(redisDataList: SaveRedisLogsDto[]) {
		const queryRunner = this.dataSource.createQueryRunner();
		await queryRunner.connect();
		await queryRunner.startTransaction();

		try {
			for (const redisData of redisDataList) {
				const { role, content, user_id, chat_room_id, created_time } = redisData;

				const chatRoom = await this.findNewChatRoom(chat_room_id);
				if (!chatRoom) throw new BadRequestException(ChatsExeption.CHAT_ROOM_NOT_EXISTS);

				if (role === 'user') {
					const newChatLog = this.chatLogRepository.create({
						question: content,
						chat_room: chatRoom,
						num_response_regen: 0,
					});

					await queryRunner.manager.save(newChatLog);
				} else if (role === 'assistant') {
					const chatLog = await queryRunner.manager
						.createQueryBuilder(ChatLog, 'chatLog')
						.leftJoinAndSelect('chatLog.chat_room', 'chatRoom')
						.where('chatRoom.id = :chatRoomId', { chatRoomId: chatRoom.id })
						.orderBy('chatLog.id', 'DESC')
						.getOne();

					if (chatLog) {
						const newModelAnswer = this.modelAnswerRepository.create({
							answer: content,
							response_time: created_time,
							chatLog: chatLog,
						});

						await queryRunner.manager.save(newModelAnswer);
					}
				}
			}
			await queryRunner.commitTransaction();
		} catch (e) {
			await queryRunner.rollbackTransaction();
			throw e;
		} finally {
			// 트랜잭션 종료 후 queryRunner 해제
			await queryRunner.release();
		}
	}

	async getLastCreatedTime(chatRoomId: string) {
		const chatRoom = await this.findNewChatRoom(Number(chatRoomId));
		if (!chatRoom) throw new BadRequestException(ChatsExeption.CHAT_ROOM_NOT_EXISTS);

		const lastLog = await this.chatLogRepository.findOne({
			where: {
				chat_room: { id: chatRoom.id },
			},
			order: { id: 'DESC' },
		});
		if (!lastLog) throw new BadRequestException(ChatsExeption.CHAT_LOG_NOT_EXISTS);

		const lastAnswer = await this.modelAnswerRepository.findOne({
			where: {
				chatLog: { id: lastLog.id },
			},
		});

		return {
			chatRoomId,
			lastCreatedTime: lastAnswer.response_time,
		};
	}
}
