import { Column, Entity } from 'typeorm';
import { BaseEntity } from '../../global/entities/base.entity';
import { PersonaStatus } from '../enums/persona-status.enum';

@Entity()
export class personaList extends BaseEntity {
	@Column()
	name: string;

	@Column()
	description: string;

	@Column()
	image_url: string;

	@Column({
		default: 0,
	})
	popular: number;

	@Column({
		type: 'enum',
		enum: PersonaStatus,
		default: 'act',
	})
	status: PersonaStatus;
}
