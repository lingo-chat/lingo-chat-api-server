import { Body, Controller, Get, Param, Post, UseFilters, UseGuards } from '@nestjs/common';
import { ChatsService } from './chats.service';
import { ResponseMessage } from 'src/global/decorators/response-key.decorator';
import { ChatsResponseMessage } from './classes/chats.response.message';
import { AtGuard } from 'src/auth/guard/access.token.guard';
import { GetUser } from 'src/global/decorators/get-user.decorator';
import { User } from 'src/users/entities/user.entity';
import { SaveRedisLogsDto } from './dtos/save-redis-logs.dto';
import { HttpExceptionFilter } from 'src/global/filters/http-exception.filter';
import { JwtExceptionFilter } from 'src/global/filters/jwt-exception.filter';

@Controller('chats')
@UseFilters(HttpExceptionFilter, JwtExceptionFilter)
export class ChatsController {
	constructor(private readonly chatsService: ChatsService) {}

	@Post('receive-message')
	@ResponseMessage(ChatsResponseMessage.CREATE_CHATROOM)
	// @UseGuards(AtGuard)
	async receiveMessage(@Body() body: { userId: string; socketId: string; message: string; personaId: number }) {
		return await this.chatsService.processFistChatMessage(body.userId, body.message, body.personaId);
	}

	@Get('chat-rooms')
	@ResponseMessage(ChatsResponseMessage.FIND_CHATROOMS)
	@UseGuards(AtGuard)
	async findChatRooms(@GetUser() user: User) {
		return await this.chatsService.findChatRooms(user);
	}

	@Get('redis/:chatRoomId')
	@ResponseMessage(ChatsResponseMessage.GET_REDIS_LOGS)
	@UseGuards(AtGuard)
	async getRedisLogs(@Param('chatRoomId') chatRoomId: string) {
		return await this.chatsService.getRedisLogs(chatRoomId);
	}

	/**
	 * {
	 * 		'role': 'user', || 'assistant'
	 * 		'content': '안녕하십니까',
	 * 		'user_id': '113357678301545310133',
	 * 		'chat_room_id': 76
	 * }
	 */
	@Post('db')
	@ResponseMessage(ChatsResponseMessage.SAVE_CHAT_LOGS)
	async saveChatLogs(@Body() body: { redisDataList: SaveRedisLogsDto[] }) {
		const { redisDataList } = body;
		return await this.chatsService.saveChatLogs(redisDataList);
	}

	@Get('db/:chatRoomId')
	@ResponseMessage(ChatsResponseMessage.GET_DB_LOGS)
	@UseGuards(AtGuard)
	async getDBLogs(@Param('chatRoomId') chatRoomId: string, @GetUser() user: User) {
		return await this.chatsService.getDBLogs(chatRoomId, user);
	}

	@Get('db/ai/:chatRoomId')
	@ResponseMessage(ChatsResponseMessage.GET_DB_LOGS)
	async getDBLogsToAI(@Param('chatRoomId') chatRoomId: string) {
		return await this.chatsService.getDBLogs(chatRoomId);
	}

	@Get('db/ai/:chatRoomId/created-time')
	@ResponseMessage(ChatsResponseMessage.GET_LAST_CREATED_TIME)
	async getLastCreatedTime(@Param('chatRoomId') chatRoomId: string) {
		return await this.chatsService.getLastCreatedTime(chatRoomId);
	}
}
