/**
 * WebBuilder API client for Natural Language to GitHub Issue generation
 */

import { API_BASE_URL } from '../config';

// TypeScript interfaces matching backend models

export interface GitHubIssue {
  title: string;
  body: string;
  labels: string[];
  classification: 'feature' | 'bug' | 'chore';
  workflow: string;
  model_set: 'base' | 'heavy';
  issue_number?: number;
}

export interface ProjectContext {
  path: string;
  is_new_project: boolean;
  framework?: string;
  backend?: string;
  complexity: 'low' | 'medium' | 'high';
  build_tools: string[];
  has_git: boolean;
  detected_files: string[];
}

export interface NLProcessingRequest {
  nl_input: string;
  project_path?: string;
  auto_detect_context?: boolean;
  confirm_before_post?: boolean;
}

export interface NLProcessingResponse {
  issue: GitHubIssue;
  project_context?: ProjectContext;
  confidence_score: number;
  intent_analysis: Record<string, any>;
  requirements: string[];
  processing_time_ms: number;
  error?: string;
}

export interface IssuePreviewRequest {
  issue: GitHubIssue;
  format: 'markdown' | 'terminal' | 'html';
}

export interface IssuePreviewResponse {
  formatted_preview: string;
  estimated_complexity: string;
  suggested_timeline?: string;
}

export interface GitHubPostRequest {
  issue: GitHubIssue;
  repository?: string;
  dry_run?: boolean;
}

export interface GitHubPostResponse {
  success: boolean;
  issue_number?: number;
  issue_url?: string;
  error?: string;
  posted_at?: string;
}

export interface GitHubCLIStatus {
  installed: boolean;
  authenticated: boolean;
  version?: string;
  user?: string;
  error?: string;
}

/**
 * Process natural language input to generate a GitHub issue
 */
export async function processNaturalLanguage(
  request: NLProcessingRequest
): Promise<NLProcessingResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/webbuilder/process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: NLProcessingResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error processing natural language:', error);
    throw error;
  }
}

/**
 * Preview a formatted GitHub issue before posting
 */
export async function previewIssue(
  request: IssuePreviewRequest
): Promise<IssuePreviewResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/webbuilder/preview`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: IssuePreviewResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error previewing issue:', error);
    throw error;
  }
}

/**
 * Get project context for a given directory
 */
export async function getProjectContext(
  path: string = '.'
): Promise<ProjectContext> {
  try {
    const params = new URLSearchParams({ path });
    const response = await fetch(
      `${API_BASE_URL}/api/webbuilder/context?${params}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: ProjectContext = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting project context:', error);
    throw error;
  }
}

/**
 * Post an issue to GitHub
 */
export async function postIssueToGitHub(
  request: GitHubPostRequest
): Promise<GitHubPostResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/webbuilder/post`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: GitHubPostResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error posting issue to GitHub:', error);
    throw error;
  }
}

/**
 * Check GitHub CLI installation and authentication status
 */
export async function checkGitHubCLIStatus(): Promise<GitHubCLIStatus> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/webbuilder/gh-status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: GitHubCLIStatus = await response.json();
    return data;
  } catch (error) {
    console.error('Error checking GitHub CLI status:', error);
    return {
      installed: false,
      authenticated: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Helper function to format issue for display
 */
export function formatIssueForDisplay(issue: GitHubIssue): string {
  const sections = [
    `# ${issue.title}`,
    '',
    `**Type:** ${issue.classification}`,
    `**Workflow:** ${issue.workflow} (${issue.model_set})`,
    `**Labels:** ${issue.labels.join(', ')}`,
    '',
    '## Body',
    issue.body,
  ];

  return sections.join('\n');
}

/**
 * Helper function to validate natural language input
 */
export function validateNLInput(input: string): {
  isValid: boolean;
  error?: string;
} {
  if (!input || input.trim().length === 0) {
    return {
      isValid: false,
      error: 'Input cannot be empty',
    };
  }

  if (input.trim().length < 10) {
    return {
      isValid: false,
      error: 'Input is too short. Please provide more details.',
    };
  }

  if (input.length > 5000) {
    return {
      isValid: false,
      error: 'Input is too long. Please limit to 5000 characters.',
    };
  }

  return { isValid: true };
}

/**
 * Helper function to get workflow description
 */
export function getWorkflowDescription(workflow: string): string {
  const descriptions: Record<string, string> = {
    adw_simple_iso: 'Simple workflow for basic tasks',
    adw_plan_build_test_iso: 'Plan, build, and test workflow for structured development',
    adw_sdlc_iso: 'Full SDLC workflow for complex implementations',
  };

  return descriptions[workflow] || 'Custom workflow';
}

/**
 * Helper function to get issue type color for UI
 */
export function getIssueTypeColor(classification: string): string {
  const colors: Record<string, string> = {
    feature: '#28a745',  // Green
    bug: '#dc3545',      // Red
    chore: '#6c757d',    // Gray
  };

  return colors[classification] || '#007bff';  // Default blue
}

/**
 * Helper function to estimate time from complexity
 */
export function estimateTimeFromComplexity(complexity: string): string {
  const estimates: Record<string, string> = {
    low: '< 1 day',
    medium: '1-3 days',
    high: '3-5 days',
  };

  return estimates[complexity] || 'TBD';
}