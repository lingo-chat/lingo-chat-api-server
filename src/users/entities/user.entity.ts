import { Column, Entity, UpdateDateColumn } from 'typeorm';
import { BaseEntity } from 'src/global/entities/base.entity';
import { UserRole } from '../enums/user-role.enum';

@Entity()
export class User extends BaseEntity {
	@Column()
	provider: string;

	@Column()
	provide_id: string;

	@Column()
	email: string;

	@Column()
	name: string;

	@Column({
		type: 'enum',
		enum: UserRole,
		default: 'user',
	})
	role: UserRole;

	@Column()
	visit_count: number;

	@UpdateDateColumn()
	last_visit_date: Date;

	@Column({ nullable: true })
	refresh_token: string;
}
