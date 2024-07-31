import { Test, TestingModule } from '@nestjs/testing';
import { WebsocketClientGateway } from './websocket-client.gateway';

describe('WebsocketClientGateway', () => {
  let gateway: WebsocketClientGateway;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [WebsocketClientGateway],
    }).compile();

    gateway = module.get<WebsocketClientGateway>(WebsocketClientGateway);
  });

  it('should be defined', () => {
    expect(gateway).toBeDefined();
  });
});
