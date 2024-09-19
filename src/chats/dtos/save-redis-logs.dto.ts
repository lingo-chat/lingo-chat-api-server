import { IsNotEmpty, IsString, IsNumber, IsOptional } from 'class-validator';

export class SaveRedisLogsDto {
	@IsString()
	@IsNotEmpty({ message: 'role은 필수값입니다..' })
	role: string;

	@IsString()
	@IsNotEmpty({ message: 'content는 필수값입니다.' })
	content: string;

	@IsString()
	@IsNotEmpty({ message: 'user_id는 필수값입니다.' })
	user_id: string;

	@IsNumber()
	@IsNotEmpty({ message: 'chat_room_id는 필수값입니다.' })
	chat_room_id: number;

	@IsString()
	@IsOptional()
	created_time?: string;
}
