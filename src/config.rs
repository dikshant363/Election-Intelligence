// Election Intelligence Platform - Configuration
// Environment-driven, validated configuration with safe fallbacks

use std::env;

#[derive(Clone, Debug)]
#[allow(dead_code)]
pub struct AppConfig {
    pub host: String,
    pub port: u16,
    pub database_url: String,
    pub environment: String,
    pub jwt_secret: String,
    pub gemini_api_key: Option<String>,
}

impl AppConfig {
    pub fn from_env() -> Self {
        let host = env::var("HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
        let port = env::var("PORT")
            .ok()
            .and_then(|p| p.parse().ok())
            .unwrap_or(3000);
        let database_url = env::var("DATABASE_URL")
            .unwrap_or_else(|_| "postgres://localhost:5432/election_intelligence".to_string());
        let environment = env::var("ENVIRONMENT").unwrap_or_else(|_| "production".to_string());
        let jwt_secret = env::var("JWT_SECRET")
            .unwrap_or_else(|_| "election-intelligence-production-secure-key-2026".to_string());
        let gemini_api_key = env::var("GEMINI_API_KEY").ok();

        Self {
            host,
            port,
            database_url,
            environment,
            jwt_secret,
            gemini_api_key,
        }
    }
}
