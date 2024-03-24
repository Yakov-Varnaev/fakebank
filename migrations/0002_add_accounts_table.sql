CREATE TABLE accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id),
  balance decimal NOT NULL DEFAULT 0
)

CREATE CONSTRAINT fk_accounts_users
  FOREIGN KEY (user_id)
  REFERENCES users(id)
  ON DELETE CASCADE;
