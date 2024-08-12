import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { RedisStorageService } from 'src/redis/redis-storage.service';
import { ChatsService } from './chats.service';
import { ResponseMessage } from 'src/global/decorators/response-key.decorator';
import { ChatResponseMessage } from './classes/chat.response.message';
import { AtGuard } from 'src/auth/guard/access.token.guard';
import { GetUser } from 'src/global/decorators/get-user.decorator';
import { User } from 'src/users/entities/user.entity';

@Controller('chats')
export class ChatsController {
	constructor(
		private readonly redisStorageService: RedisStorageService,
		private readonly chatsService: ChatsService,
	) {}

	@Post('receive-message')
	@ResponseMessage(ChatResponseMessage.CREATE_CHATROOM)
	async receiveMessage(@Body() body: { providerId: string; socketId: string; message: string; personaId: number }) {
		console.log('Received message from user:', body.providerId, body.message);
		return await this.chatsService.processChatMessage(body.providerId, body.message, body.personaId);
	}

	@Get('chat-rooms')
	@ResponseMessage(ChatResponseMessage.FIND_CHATROOMS)
	@UseGuards(AtGuard)
	async findChatRooms(@GetUser() user: User) {
		return await this.chatsService.findChatRooms(user);
	}
}
