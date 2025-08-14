const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Starting build process...');

// Install and build from root using react-app-rewired
console.log('Building React app...');
try {
  execSync('react-scripts build', { 
    stdio: 'inherit',
    env: { 
      ...process.env,
      PUBLIC_URL: '',
      BUILD_PATH: 'build'
    }
  });
  console.log('Build process completed successfully!');
} catch (error) {
  console.error('Build failed:', error.message);
  process.exit(1);
}
