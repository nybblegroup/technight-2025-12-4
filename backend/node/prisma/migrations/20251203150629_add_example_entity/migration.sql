-- CreateTable
CREATE TABLE "example" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(200) NOT NULL,
    "title" VARCHAR(200) NOT NULL,
    "entry_date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "description" VARCHAR(1000),
    "is_active" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "example_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "ix_example_entry_date" ON "example"("entry_date");
