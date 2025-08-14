const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Starting build process...');

// Change to frontend directory and build
process.chdir('FullStackApp/frontend');
console.log('Installing dependencies...');
execSync('npm install', { stdio: 'inherit' });

console.log('Building React app...');
execSync('npm run build', { stdio: 'inherit' });

// Copy build folder to root
console.log('Copying build files to root...');
const sourceDir = path.join(process.cwd(), 'build');
const targetDir = path.join(process.cwd(), '../../build');

// Create target directory if it doesn't exist
if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}

// Copy all files from source to target
function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest);
    }
    fs.readdirSync(src).forEach(childItemName => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

copyRecursiveSync(sourceDir, targetDir);
console.log('Build process completed successfully!');
