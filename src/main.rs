// Election Intelligence Platform - Main Application Entrypoint
// Pure Rust Full-Stack Architecture (Axum + Tokio + SQLx + PostgreSQL + Leptos/SSR)

mod ai;
mod api;
mod audit;
mod config;
mod db;
mod domain;
mod error;
pub mod ingestion;
mod search;
mod ui;

use ai::GroundedAIEngine;
use api::{create_api_router, AppState};
use config::AppConfig;
use db::Database;
use search::BM25Index;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::sync::RwLock;
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Initialize Tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,election_intelligence=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    tracing::info!(
        "Initializing Election Intelligence Platform v1.0.0 (Pure Rust Architecture)..."
    );

    // 2. Load Configuration
    let config = AppConfig::from_env();
    tracing::info!(
        host = %config.host,
        port = %config.port,
        environment = %config.environment,
        "Configuration loaded"
    );

    // 3. Connect to PostgreSQL
    let db = Database::connect(&config.database_url).await.map_err(|e| {
        tracing::error!(
            "Failed to connect to PostgreSQL at {}: {:?}",
            config.database_url,
            e
        );
        e
    })?;
    tracing::info!("Connected to PostgreSQL database with connection pooling");

    // 4. Build in-memory BM25 Search Index from PostgreSQL documents
    let search_docs = db.get_search_documents().await.unwrap_or_default();
    tracing::info!(count = %search_docs.len(), "Indexed electoral entities into BM25 ranker");
    let search_index = Arc::new(RwLock::new(BM25Index::build(search_docs)));

    // 5. Initialize Grounded AI Engine
    let ai_engine = Arc::new(GroundedAIEngine::new(config.gemini_api_key.clone()));

    // 6. Build AppState
    let state = AppState {
        db: db.clone(),
        ai: ai_engine,
        search_index,
    };

    // 7. Setup Web Application & API Routes
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = axum::Router::new()
        .route(
            "/",
            axum::routing::get(|| async { axum::response::Html(ui::render_homepage()) }),
        )
        .route(
            "/candidates",
            axum::routing::get(|| async { axum::response::Html(ui::render_candidates()) }),
        )
        .route(
            "/constituencies",
            axum::routing::get(|| async { axum::response::Html(ui::render_constituencies()) }),
        )
        .route(
            "/results",
            axum::routing::get(|| async { axum::response::Html(ui::render_results()) }),
        )
        .route(
            "/ai",
            axum::routing::get(|| async { axum::response::Html(ui::render_ai()) }),
        )
        .route(
            "/evidence",
            axum::routing::get(|| async { axum::response::Html(ui::render_evidence()) }),
        )
        .route(
            "/community",
            axum::routing::get(|| async { axum::response::Html(ui::render_community()) }),
        )
        .route(
            "/admin",
            axum::routing::get(|| async { axum::response::Html(ui::render_admin()) }),
        )
        .merge(create_api_router(state))
        .fallback(|| async { axum::response::Html(ui::render_homepage()) })
        .layer(cors)
        .layer(TraceLayer::new_for_http());

    // 8. Start HTTP Server
    let addr: SocketAddr = format!("{}:{}", config.host, config.port).parse()?;
    tracing::info!("Election Intelligence Platform running at http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app)
        .with_graceful_shutdown(shutdown_signal())
        .await?;

    tracing::info!("Server shut down gracefully");
    Ok(())
}

async fn shutdown_signal() {
    let ctrl_c = async {
        tokio::signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        tokio::signal::unix::signal(tokio::signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }
}
