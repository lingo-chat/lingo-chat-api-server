import { Column, Entity, ManyToOne, JoinColumn } from 'typeorm';
import { BaseEntity } from 'src/global/entities/base.entity';
import { ChatLog } from './chatLog.entity';

@Entity()
export class ModelAnswer extends BaseEntity {
	@Column()
	answer: string;

	@Column()
	response_time: string;

	@ManyToOne(() => ChatLog)
	@JoinColumn({ name: 'chat_log_id' })
	chatLog: ChatLog;
}
