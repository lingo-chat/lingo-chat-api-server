import { Module } from '@nestjs/common';
import { PersonaController } from './persona.controller';
import { PersonaService } from './persona.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import { personaList } from './entities/personaList.entity';

@Module({
	imports: [TypeOrmModule.forFeature([personaList])],
	controllers: [PersonaController],
	providers: [PersonaService],
})
export class PersonaModule {}
