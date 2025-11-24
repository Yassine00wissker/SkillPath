-- Migration: Add role column to users table
-- Run this SQL script to add the role column to existing database

USE skillpath;

-- Add role column with default value 'user'
ALTER TABLE users 
ADD COLUMN role VARCHAR(50) DEFAULT 'user' AFTER password;

-- Update existing users to have 'user' role (if not already set)
UPDATE users SET role = 'user' WHERE role IS NULL OR role = '';

-- Verify the column was added
DESCRIBE users;

