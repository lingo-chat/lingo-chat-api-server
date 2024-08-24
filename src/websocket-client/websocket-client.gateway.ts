import { ConfigService } from '@nestjs/config';
import {
	OnGatewayConnection,
	OnGatewayDisconnect,
	SubscribeMessage,
	WebSocketGateway,
	WebSocketServer,
} from '@nestjs/websockets';
import { Server } from 'socket.io';
import { io, Socket } from 'socket.io-client';

@WebSocketGateway({
	cors: {
		origin: '*', // 실제 배포 시에는 보안을 위해 특정 도메인으로 제한
	},
})
export class WebsocketClientGateway implements OnGatewayConnection, OnGatewayDisconnect {
	@WebSocketServer()
	server: Server;
	private socket: Socket;

	constructor(private readonly configService: ConfigService) {}

	onModuleInit() {
		const socketServerUrl = this.configService.getOrThrow('SOCKET_SERVER_URL');
		this.socket = io(socketServerUrl);
		this.socket.on('connect', () => {
			console.log('Connected to socket server');
		});
	}

	afterInit() {
		console.log('WebSocket client initialized');
	}

	handleConnection() {
		console.log('API server connected to socket server');
	}

	handleDisconnect() {
		console.log('API server disconnected from socket server');
	}

	sendMessageToSocketServer(event: string, data: any) {
		this.socket.emit(event, data);
	}

	sendNewChatRoom(event: string, data: any) {
		this.socket.emit(event, data);
	}
}
