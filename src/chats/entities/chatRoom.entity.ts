import { Column, Entity, ManyToOne, JoinColumn } from 'typeorm';
import { BaseEntity } from 'src/global/entities/base.entity';
import { User } from 'src/users/entities/user.entity';
import { personaList } from 'src/persona/entities/personaList.entity';

@Entity()
export class ChatRoom extends BaseEntity {
	@Column()
	title: string;

	@ManyToOne(() => User)
	@JoinColumn({ name: 'user_id' })
	user: User;

	@ManyToOne(() => personaList)
	@JoinColumn({ name: 'persona_id' })
	persona: personaList;
}
