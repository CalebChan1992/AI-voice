// Simple script to run frontend tests
const { execSync } = require('child_process');
const path = require('path');

// Get the root directory
const rootDir = path.resolve(__dirname, '../..');
const frontendDir = path.join(rootDir, 'frontend');

// Run the tests
try {
  console.log('Running frontend tests...');
  
  // Create a temporary test file in the frontend directory that imports our tests
  const testContent = `
  // This file imports all tests from the test directory
  import './components/ExampleComponent.test';
  import './unit/auth.test';
  `;
  
  // Run the tests using Vitest
  const result = execSync('cd ../../frontend && npx vitest run', {
    stdio: 'inherit',
    cwd: __dirname
  });
  
  console.log('Tests completed successfully!');
} catch (error) {
  console.error('Error running tests:', error.message);
  process.exit(1);
}
