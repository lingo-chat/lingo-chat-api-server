import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { ChatRoom } from './entities/chatRoom.entity';
import { Repository } from 'typeorm';
import { WebsocketClientGateway } from 'src/websocket-client/websocket-client.gateway';
import { PersonaService } from 'src/persona/persona.service';
import { UsersService } from 'src/users/users.service';
import { personaList } from 'src/persona/entities/personaList.entity';
import { User } from 'src/users/entities/user.entity';

@Injectable()
export class ChatsService {
	constructor(
		private readonly personaService: PersonaService,
		private readonly usersService: UsersService,
		@InjectRepository(ChatRoom)
		private readonly chatRoomRepository: Repository<ChatRoom>,
	) {}

	async processChatMessage(providerId: string, message: string, personaId: number) {
		const persona = await this.personaService.getPersona(personaId);
		const personaName = persona.name;

		const title = await this.createChatTitle(message, personaName);
		const chatRoom = await this.createChatRoom(providerId, title, persona);

		// AI 서버로부터 답변 받아오는 임시 코드
		const url = 'https://fa9e-121-130-44-227.ngrok-free.app/v1/chat/completions';
		const apiKey = 'test_api_key';
		const sendData = {
			model: '/home/iwbaporandhh/huggingface/models/llama-3-ko-8B-science-chat',
			messages: [
				{ role: 'system', content: '너의 이름은 궤도입니다.' },
				{ role: 'user', content: '안녕하세요, 테스트 메세지입니다. 당신의 이름은 무엇인가요?' },
			],
			temperature: 0.6,
			top_p: 0.9,
			frequency_penalty: 1.4,
			max_tokens: 2048, // == completion tokens
			seed: 42,
			stream: false,
			stop: ['</s>'],
		};

		await fetch(url, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${apiKey}`,
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(sendData),
		})
			.then((response) => response.json())
			.then((result) => {
				if (result.choices && result.choices.length > 0) {
					console.log(result.choices[0].message.content);
				} else {
					console.error('Unexpected response structure:', result);
				}
			})
			.catch((error) => {
				console.error('Error:', error);
			});

		return {
			chatRoomId: chatRoom.id,
			title: chatRoom.title,
		};
	}

	private async createChatTitle(message: string, personaName: string) {
		const truncatedMessage = message.substring(0, 10);
		return personaName + `-` + truncatedMessage;
	}

	private async createChatRoom(providerId: string, title: string, persona: personaList) {
		const user = await this.usersService.findUser({ provide_id: providerId });

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
}
