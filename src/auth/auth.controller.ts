import { Controller, Get, Post, Req, Res, UseFilters, UseGuards } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthGuard } from '@nestjs/passport';
import { Request } from 'express';
import { ResponseMessage } from 'src/global/decorators/response-key.decorator';
import { AuthReponseMessage } from './classes/auth.response.message';
import { GetUser } from 'src/global/decorators/get-user.decorator';
import { User } from 'src/users/entities/user.entity';
import { JwtExceptionFilter } from 'src/global/filters/jwt-exception.filter';
import { RtGuard } from './guard/refresh.token.guard';

@Controller('auth')
@UseFilters(JwtExceptionFilter)
export class AuthController {
	constructor(private readonly authService: AuthService) {}

	@Get('google')
	@UseGuards(AuthGuard('google'))
	async googleLogin() {}

	@Get('google/callback')
	@UseGuards(AuthGuard('google'))
	@ResponseMessage(AuthReponseMessage.LOG_IN)
	async googleLoginCallback(@Req() req: Request) {
		return await this.authService.googleOAuthLogin({ req });
	}

	@Post('refresh')
	@UseGuards(RtGuard)
	@ResponseMessage(AuthReponseMessage.REFRESH)
	async refresh(@GetUser() user: User) {
		return await this.authService.refresh(user);
	}
}
