#!/usr/bin/env python3
"""
Import Path Standardization Script
Fixes import inconsistencies across the UOR Evolution repository
"""

import os
import re
import ast
from pathlib import Path
from typing import List, Dict, Set, Tuple
import argparse


class ImportAnalyzer:
    """Analyzes and fixes import statements in Python files"""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.issues = []
        self.fixes_applied = 0
        
    def scan_repository(self) -> Dict[str, List[str]]:
        """Scan all Python files for import issues"""
        issues = {
            'relative_imports': [],
            'missing_modules': [],
            'circular_dependencies': [],
            'inconsistent_paths': []
        }
        
        python_files = list(self.repo_root.rglob("*.py"))
        
        for file_path in python_files:
            if self._should_skip_file(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                file_issues = self._analyze_file_imports(file_path, content)
                for issue_type, file_issues_list in file_issues.items():
                    issues[issue_type].extend(file_issues_list)
                    
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
                
        return issues
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_patterns = [
            '__pycache__',
            '.git',
            'venv',
            'env',
            '.pytest_cache',
            'node_modules'
        ]
        
        return any(pattern in str(file_path) for pattern in skip_patterns)
    
    def _analyze_file_imports(self, file_path: Path, content: str) -> Dict[str, List[str]]:
        """Analyze imports in a single file"""
        issues = {
            'relative_imports': [],
            'missing_modules': [],
            'circular_dependencies': [],
            'inconsistent_paths': []
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    issue = self._check_import_node(file_path, node)
                    if issue:
                        issue_type, description = issue
                        issues[issue_type].append(f"{file_path}: {description}")
                        
        except SyntaxError as e:
            issues['missing_modules'].append(f"{file_path}: Syntax error - {e}")
            
        return issues
    
    def _check_import_node(self, file_path: Path, node) -> Tuple[str, str] or None:
        """Check a single import node for issues"""
        if isinstance(node, ast.ImportFrom):
            if node.module:
                # Check for relative imports
                if node.level > 0:
                    return ('relative_imports', f"Relative import: {node.module}")
                
                # Check for inconsistent module paths
                if node.module.startswith('modules.') and not self._is_valid_module_path(node.module):
                    return ('inconsistent_paths', f"Invalid module path: {node.module}")
                    
        return None
    
    def _is_valid_module_path(self, module_path: str) -> bool:
        """Check if a module path is valid"""
        # Convert module path to file path
        parts = module_path.split('.')
        potential_path = self.repo_root / '/'.join(parts)
        
        # Check if it's a package (has __init__.py) or a module (.py file)
        return (potential_path.with_suffix('.py').exists() or 
                (potential_path / '__init__.py').exists())
    
    def fix_imports_in_file(self, file_path: Path) -> bool:
        """Fix import issues in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix relative imports
            content = self._fix_relative_imports(content, file_path)
            
            # Fix inconsistent module paths
            content = self._fix_module_paths(content)
            
            # Fix common import patterns
            content = self._fix_common_patterns(content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied += 1
                return True
                
        except Exception as e:
            print(f"Error fixing imports in {file_path}: {e}")
            
        return False
    
    def _fix_relative_imports(self, content: str, file_path: Path) -> str:
        """Convert relative imports to absolute imports"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Match relative imports like "from .module import" or "from ..module import"
            relative_pattern = r'^(\s*)from\s+(\.+)([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s+import\s+(.+)$'
            match = re.match(relative_pattern, line)
            
            if match:
                indent, dots, module, imports = match.groups()
                
                # Calculate absolute module path
                abs_module = self._calculate_absolute_module(file_path, dots, module)
                if abs_module:
                    fixed_line = f"{indent}from {abs_module} import {imports}"
                    fixed_lines.append(fixed_line)
                    continue
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _calculate_absolute_module(self, file_path: Path, dots: str, module: str) -> str:
        """Calculate absolute module path from relative import"""
        # Get the package path relative to repo root
        rel_path = file_path.relative_to(self.repo_root)
        package_parts = rel_path.parent.parts
        
        # Calculate how many levels to go up
        levels_up = len(dots)
        
        if levels_up > len(package_parts):
            return None  # Invalid relative import
        
        # Build absolute module path
        if levels_up == 1:
            # Same package
            base_parts = package_parts
        else:
            # Go up levels
            base_parts = package_parts[:-levels_up + 1]
        
        if module:
            full_module = '.'.join(base_parts + tuple(module.split('.')))
        else:
            full_module = '.'.join(base_parts)
        
        return full_module
    
    def _fix_module_paths(self, content: str) -> str:
        """Fix inconsistent module paths"""
        # Common module path fixes
        fixes = {
            r'from modules\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*) import': 
                r'from modules.\1 import',
            r'import modules\.([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)':
                r'import modules.\1',
        }
        
        for pattern, replacement in fixes.items():
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _fix_common_patterns(self, content: str) -> str:
        """Fix common import patterns and issues"""
        # Remove duplicate imports
        lines = content.split('\n')
        seen_imports = set()
        fixed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Check if it's an import line
            if (stripped.startswith('import ') or stripped.startswith('from ')) and stripped not in seen_imports:
                seen_imports.add(stripped)
                fixed_lines.append(line)
            elif not (stripped.startswith('import ') or stripped.startswith('from ')):
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def generate_report(self, issues: Dict[str, List[str]]) -> str:
        """Generate a report of import issues"""
        report = ["Import Analysis Report", "=" * 50, ""]
        
        for issue_type, issue_list in issues.items():
            if issue_list:
                report.append(f"{issue_type.replace('_', ' ').title()}: {len(issue_list)} issues")
                for issue in issue_list[:10]:  # Show first 10 issues
                    report.append(f"  - {issue}")
                if len(issue_list) > 10:
                    report.append(f"  ... and {len(issue_list) - 10} more")
                report.append("")
        
        report.append(f"Total fixes applied: {self.fixes_applied}")
        
        return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(description='Fix import issues in UOR Evolution repository')
    parser.add_argument('--repo-root', default='.', help='Repository root directory')
    parser.add_argument('--fix', action='store_true', help='Apply fixes (default: analyze only)')
    parser.add_argument('--report', default='import_analysis_report.txt', help='Report output file')
    
    args = parser.parse_args()
    
    analyzer = ImportAnalyzer(args.repo_root)
    
    print("Scanning repository for import issues...")
    issues = analyzer.scan_repository()
    
    if args.fix:
        print("Applying fixes...")
        python_files = list(Path(args.repo_root).rglob("*.py"))
        
        for file_path in python_files:
            if not analyzer._should_skip_file(file_path):
                analyzer.fix_imports_in_file(file_path)
    
    # Generate and save report
    report = analyzer.generate_report(issues)
    
    with open(args.report, 'w') as f:
        f.write(report)
    
    print(f"Analysis complete. Report saved to {args.report}")
    print(f"Fixes applied: {analyzer.fixes_applied}")


if __name__ == '__main__':
    main()
