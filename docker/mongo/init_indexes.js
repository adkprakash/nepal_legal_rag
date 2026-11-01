const dbName = process.env.MONGO_DB_NAME;
const adminRwPassword = process.env.MONGO_ADMIN_RW_PASSWORD;
const userAppPassword = process.env.MONGO_USER_APP_PASSWORD;

if (!dbName || !adminRwPassword || !userAppPassword) {
  throw new Error("Missing MONGO_DB_NAME / MONGO_ADMIN_RW_PASSWORD / MONGO_USER_APP_PASSWORD");
}

const appDb = db.getSiblingDB(dbName);

// User service: read the laws, manage its own accounts, write only its own logs
appDb.createRole({
  role: "userServiceRole",
  privileges: [
    { resource: { db: dbName, collection: "documents" },  actions: ["find"] },
    { resource: { db: dbName, collection: "chunks" },     actions: ["find"] },
    { resource: { db: dbName, collection: "users" },      actions: ["find", "insert", "update"] },
    { resource: { db: dbName, collection: "query_logs" }, actions: ["find", "insert"] }
  ],
  roles: []
});

appDb.createUser({
  user: "admin_rw",
  pwd: adminRwPassword,
  roles: [{ role: "readWrite", db: dbName }]
});

appDb.createUser({
  user: "user_app",
  pwd: userAppPassword,
  roles: [{ role: "userServiceRole", db: dbName }]
});

appDb.documents.createIndex({ document_id: 1 }, { unique: true });
appDb.documents.createIndex({ category: 1 });
appDb.documents.createIndex({ status: 1 });

appDb.chunks.createIndex({ chunk_id: 1 }, { unique: true });
appDb.chunks.createIndex({ document_id: 1 });
appDb.chunks.createIndex({ section: 1 });

appDb.ingestion_jobs.createIndex({ job_id: 1 }, { unique: true });
appDb.ingestion_jobs.createIndex({ document_id: 1 });
appDb.ingestion_jobs.createIndex({ status: 1, created_at: -1 });

appDb.users.createIndex({ user_id: 1 }, { unique: true });
appDb.users.createIndex({ email: 1 }, { unique: true });

appDb.query_logs.createIndex({ trace_id: 1 }, { unique: true });
appDb.query_logs.createIndex({ created_at: -1 });

print("init_indexes.js finished for database " + dbName);