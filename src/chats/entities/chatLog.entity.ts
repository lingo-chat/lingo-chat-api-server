import { Column, Entity, OneToOne, JoinColumn, OneToMany, ManyToOne } from 'typeorm';
import { BaseEntity } from 'src/global/entities/base.entity';
import { ChatRoom } from './chatRoom.entity';
import { ModelAnswer } from './modelAnswer.entity';

@Entity()
export class ChatLog extends BaseEntity {
	@Column()
	question: string;

	@Column()
	num_response_regen: number;

	@ManyToOne(() => ChatRoom)
	@JoinColumn({ name: 'chat_room_id' })
	chat_room: ChatRoom;
}
