import * as Joi from 'joi';

export const validationSchema = Joi.object({
	// SERVER
	SERVER_PORT: Joi.number().required(),

	// POSTGRESQL
	POSTGRESQL_USER: Joi.string().required(),
	POSTGRESQL_PASSWORD: Joi.string().required(),
	POSTGRESQL_HOST: Joi.string().required(),
	POSTGRESQL_PORT: Joi.number().required(),
	POSTGRESQL_DATABASE: Joi.string().required(),
	POSTGRESQL_SYNCHRONIZE: Joi.boolean().required(),
	POSTGRESQL_LOGGING: Joi.boolean().required(),

	// REDIS
	REDIS_HOST: Joi.string().required(),
	REDIS_PORT: Joi.number().required(),
	REDIS_DB: Joi.number().required(),

	// GOOGLE OAUTH
	OAUTH_GOOGLE_CLIENT_ID: Joi.string().required(),
	OAUTH_GOOGLE_SECRET: Joi.string().required(),
	OAUTH_GOOGLE_REDIRECT: Joi.string().required(),

	// JWT
	JWT_ACCESS_SECRET_KEY: Joi.string().required(),
	JWT_ACCESS_EXPIRATION_TIME: Joi.number().required(),
	JWT_REFRESH_SECRET_KEY: Joi.string().required(),
	JWT_REFRESH_EXPIRATION_TIME: Joi.number().required(),

	// VAULT
	VAULT_ENDPOINT: Joi.string().required(),
	VAULT_TOKEN: Joi.string().required(),

	// REACT_APP
	REACT_APP_BASE: Joi.string().required(),

	// SOCKET_SERVER
	SOCKET_SERVER_URL: Joi.string().required(),
});
