import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { personaList } from './entities/personaList.entity';

@Injectable()
export class PersonaService {
	constructor(
		@InjectRepository(personaList)
		private readonly personaListRepository: Repository<personaList>,
	) {}

	async getPersonaList() {
		const personaList = await this.personaListRepository.find();
		return personaList;
	}

	async getPersona(personaId: number) {
		const persona = await this.personaListRepository.findOne({ where: { id: personaId } });
		return persona;
	}
}
