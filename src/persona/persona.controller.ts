import { Controller, Get, Param, Post } from '@nestjs/common';
import { PersonaService } from './persona.service';

@Controller('persona')
export class PersonaController {
	constructor(private readonly personaService: PersonaService) {}

	@Get()
	async getAllPersona() {
		return await this.personaService.getPersonaList();
	}

	@Get(':personaId')
	async getPersona(@Param('personaId') personaId: number) {
		return await this.personaService.getPersona(personaId);
	}
}
