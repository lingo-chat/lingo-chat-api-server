import { Module } from '@nestjs/common';
import { WebsocketClientGateway } from './websocket-client.gateway';

@Module({
	providers: [WebsocketClientGateway],
})
export class WebsocketClientModule {}
