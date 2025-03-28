#!/usr/bin/env node
/**
 * Dependency Synchronization Script
 *
 * This script helps maintain consistent dependency versions across all packages
 * in the monorepo. It generates a report of dependency versions and optionally
 * updates packages to use the same version.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const ROOT_DIR = path.resolve(__dirname, '..');
const WORKSPACE_PATTERNS = ['frontend', 'shared/*', 'infrastructure/*', 'packages/*'];
const SKIP_DEPENDENCIES = ['react-native', '@react-native']; // Skip certain dependencies

/**
 * Get all package directories based on workspace patterns
 */
function getPackageDirs() {
  const packageDirs = [];

  WORKSPACE_PATTERNS.forEach(pattern => {
    if (pattern.includes('*')) {
      const [parent] = pattern.split('/*');
      if (fs.existsSync(path.join(ROOT_DIR, parent))) {
        const subdirs = fs.readdirSync(path.join(ROOT_DIR, parent));
        subdirs.forEach(subdir => {
          const fullPath = path.join(ROOT_DIR, parent, subdir);
          if (fs.existsSync(path.join(fullPath, 'package.json'))) {
            packageDirs.push(fullPath);
          }
        });
      }
    } else {
      const fullPath = path.join(ROOT_DIR, pattern);
      if (fs.existsSync(path.join(fullPath, 'package.json'))) {
        packageDirs.push(fullPath);
      }
    }
  });

  return packageDirs;
}

/**
 * Get dependencies from a package.json file
 */
function getDependencies(packagePath) {
  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));

  const dependencies = {};

  // Combine all types of dependencies
  ['dependencies', 'devDependencies', 'peerDependencies'].forEach(depType => {
    if (packageJson[depType]) {
      Object.entries(packageJson[depType]).forEach(([name, version]) => {
        // Skip dependencies that should be ignored
        if (!SKIP_DEPENDENCIES.some(skip => name.startsWith(skip))) {
          if (!dependencies[name]) {
            dependencies[name] = [];
          }
          dependencies[name].push({
            type: depType,
            version,
            packageJson: packagePath
          });
        }
      });
    }
  });

  return {
    name: packageJson.name,
    path: packagePath,
    dependencies
  };
}

/**
 * Update a package.json file with new dependency versions
 */
function updatePackage(packagePath, updates) {
  const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
  let updated = false;

  // Update dependencies
  ['dependencies', 'devDependencies', 'peerDependencies'].forEach(depType => {
    if (packageJson[depType]) {
      Object.entries(packageJson[depType]).forEach(([name, version]) => {
        if (updates[name] && version !== updates[name]) {
          packageJson[depType][name] = updates[name];
          updated = true;
          console.log(`  Updated ${name} in ${depType} from ${version} to ${updates[name]}`);
        }
      });
    }
  });

  if (updated) {
    fs.writeFileSync(packagePath, JSON.stringify(packageJson, null, 2) + '\n');
    return true;
  }

  return false;
}

/**
 * Main function
 */
function main() {
  const updateMode = process.argv.includes('--update');
  const packageDirs = getPackageDirs();

  console.log(`Found ${packageDirs.length} packages in the monorepo.`);

  // Collect all dependencies
  const packagesData = packageDirs.map(dir =>
    getDependencies(path.join(dir, 'package.json'))
  );

  // Add root package
  packagesData.push(getDependencies(path.join(ROOT_DIR, 'package.json')));

  // Analyze dependencies
  const allDependencies = {};

  packagesData.forEach(pkg => {
    Object.entries(pkg.dependencies).forEach(([name, instances]) => {
      if (!allDependencies[name]) {
        allDependencies[name] = [];
      }
      allDependencies[name].push(...instances);
    });
  });

  // Find inconsistencies
  const inconsistentDeps = {};

  Object.entries(allDependencies).forEach(([name, instances]) => {
    const versions = [...new Set(instances.map(i => i.version))];
    if (versions.length > 1) {
      inconsistentDeps[name] = {
        versions,
        latest: versions.sort().pop(),
        instances
      };
    }
  });

  // Print report
  if (Object.keys(inconsistentDeps).length === 0) {
    console.log('✅ All dependencies are consistent across packages!');
  } else {
    console.log(`Found ${Object.keys(inconsistentDeps).length} inconsistent dependencies:`);

    Object.entries(inconsistentDeps).forEach(([name, data]) => {
      console.log(`\n📦 ${name}:`);
      data.versions.forEach(version => {
        const count = data.instances.filter(i => i.version === version).length;
        console.log(`  - ${version} (${count} packages)`);
      });
      console.log(`  Latest: ${data.latest}`);
    });

    // Update if requested
    if (updateMode) {
      console.log('\nUpdating dependencies to latest versions...');
      const updates = {};

      Object.entries(inconsistentDeps).forEach(([name, data]) => {
        updates[name] = data.latest;
      });

      let updatedCount = 0;
      packagesData.forEach(pkg => {
        console.log(`\nChecking ${pkg.name}...`);
        if (updatePackage(pkg.path, updates)) {
          updatedCount++;
        } else {
          console.log('  No updates needed');
        }
      });

      console.log(`\n✅ Updated ${updatedCount} packages.`);
      console.log('\nTo install updated dependencies, run:');
      console.log('  npm install');
    } else {
      console.log('\nTo update dependencies to the latest versions, run:');
      console.log('  node scripts/sync-dependencies.js --update');
    }
  }
}

// Run the script
main();
