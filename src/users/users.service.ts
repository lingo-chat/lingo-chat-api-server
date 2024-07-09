import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { FindOptionsWhere, Repository } from 'typeorm';
import { GoogleUser } from 'src/global/interfaces/google.user';

@Injectable()
export class UsersService {
	constructor(
		@InjectRepository(User)
		private readonly userRepository: Repository<User>,
	) {}

	async isUserExist(options: FindOptionsWhere<User>): Promise<boolean> {
		return this.userRepository.exists({ where: options });
	}

	async findUser(options: FindOptionsWhere<User>): Promise<User | null> {
		return await this.userRepository.findOne({ where: options });
	}

	async createGoogleUser(googleUser: GoogleUser) {
		const { provider, provideId, email, name } = googleUser;

		const userEmail = Object.values(email)[0];
		const userName = Object.values(name)[1];

		const newUser = {
			provider: provider,
			provide_id: provideId,
			email: userEmail,
			name: userName,
			visit_count: 1,
		};

		return await this.userRepository.save(newUser);
	}
}
