import { ExceptionObjError } from 'src/global/enums/exception-obj-error.enum';
import { ExceptionObj } from 'src/global/interfaces/exception.obj';

export class ChatsExeption {
	static CHAT_ROOM_NOT_EXISTS: ExceptionObj = {
		message: '존재하지않는 채팅방입니다.',
		error: ExceptionObjError.BAD_REQUEST,
	};
	static CHAT_LOG_NOT_EXISTS: ExceptionObj = {
		message: '채팅 로그가 존재하지 않습니다.',
		error: ExceptionObjError.BAD_REQUEST,
	};
}
