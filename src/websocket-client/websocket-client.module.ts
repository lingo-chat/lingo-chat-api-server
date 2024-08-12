import { Module } from '@nestjs/common';
import { WebsocketClientGateway } from './websocket-client.gateway';

@Module({
	providers: [WebsocketClientGateway],
	exports: [WebsocketClientGateway],
})
export class WebsocketClientModule {}
