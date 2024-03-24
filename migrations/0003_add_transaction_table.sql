CREATE TABLE transactions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id uuid NOT NULL REFERENCES accounts(id),
  recipient_id uuid NOT NULL REFERENCES accounts(id),
  amount decimal NOT NULL,
  description text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now()
);

CREATE CONSTRAINT fk_transactions_sender
  FOREIGN KEY (sender_id)
  REFERENCES accounts(id)
  ON DELETE CASCADE;

CREATE CONSTRAINT fk_transactions_recipient
  FOREIGN KEY (recipient_id)
  REFERENCES accounts(id)
  ON DELETE CASCADE;
