import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { ChatRoom } from './entities/chatRoom.entity';
import { Repository } from 'typeorm';
import { WebsocketClientGateway } from 'src/websocket-client/websocket-client.gateway';
import { PersonaService } from 'src/persona/persona.service';
import { UsersService } from 'src/users/users.service';
import { personaList } from 'src/persona/entities/personaList.entity';
import { User } from 'src/users/entities/user.entity';
import { RedisStorageService } from 'src/redis/redis-storage.service';

@Injectable()
export class ChatsService {
	constructor(
		private readonly personaService: PersonaService,
		private readonly usersService: UsersService,
		private readonly websocketClientGateway: WebsocketClientGateway,
		@InjectRepository(ChatRoom)
		private readonly chatRoomRepository: Repository<ChatRoom>,
		private readonly redisStorageService: RedisStorageService,
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

		const user_id = provideId;
		const chat_room_id = chatRoom.id;
		const user_message = message;

		const str = JSON.stringify({ user_id, chat_room_id, user_message });

		await this.redisStorageService.queue('user_ms_queue', str);

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

	// AI 서버로부터 답변 받아오는 임시 코드
	async responseAIserverTest(): Promise<string | null> {
		const url = '';
		const apiKey = '';
		const sendData = {
			model: '/home/iwbaporandhh/huggingface/models/llama-3-ko-8B-science-chat',
			messages: [
				{ role: 'system', content: '너의 이름은 궤도입니다.' },
				{ role: 'user', content: '안녕하세요, 테스트 메세지입니다. 당신의 이름은 무엇인가요?' },
			],
			temperature: 0.6,
			top_p: 0.9,
			frequency_penalty: 1.4,
			max_tokens: 2048,
			seed: 42,
			stream: false,
			stop: ['</s>'],
		};

		try {
			const response = await fetch(url, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${apiKey}`,
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(sendData),
			});

			const result = await response.json();

			if (result.choices && result.choices.length > 0) {
				const message = result.choices[0].message.content;
				return message; // 메시지를 반환합니다.
			} else {
				console.error('Unexpected response structure:', result);
				return null;
			}
		} catch (error) {
			console.error('Error:', error);
			return null;
		}
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

	async findNewChatRoom(chatRoomid: number) {
		const newChatRoom = await this.chatRoomRepository.findOne({
			where: { id: chatRoomid },
			relations: ['persona'],
		});

		return newChatRoom;
	}
}
