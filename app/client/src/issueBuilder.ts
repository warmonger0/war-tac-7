/**
 * Issue Builder Module - Vanilla TypeScript implementation for WebBuilder
 */

import {
  processNaturalLanguage,
  previewIssue,
  postIssueToGitHub,
  checkGitHubCLIStatus,
  getProjectContext,
  validateNLInput,
  getIssueTypeColor,
  estimateTimeFromComplexity,
  type NLProcessingRequest,
  type NLProcessingResponse,
  type ProjectContext,
  type GitHubCLIStatus,
  type IssuePreviewRequest,
  type GitHubPostRequest,
} from './api/webbuilder';

export class IssueBuilder {
  private container: HTMLElement;
  private nlInput: string = '';
  private projectContext: ProjectContext | null = null;
  private ghStatus: GitHubCLIStatus | null = null;
  private processingResponse: NLProcessingResponse | null = null;
  private issuePreview: string = '';

  constructor(containerId: string) {
    const element = document.getElementById(containerId);
    if (!element) {
      throw new Error(`Container element with id "${containerId}" not found`);
    }
    this.container = element;
  }

  async init(): Promise<void> {
    await this.loadInitialData();
    this.render();
  }

  private async loadInitialData(): Promise<void> {
    try {
      // Check GitHub CLI status
      this.ghStatus = await checkGitHubCLIStatus();

      // Get project context for current directory
      this.projectContext = await getProjectContext('.');
    } catch (error) {
      console.error('Failed to load initial data:', error);
    }
  }

  private render(): void {
    this.container.innerHTML = `
      <div class="issue-builder-section">
        <h2>Create GitHub Issue from Natural Language</h2>

        <div id="gh-status" class="status-container"></div>
        <div id="project-context" class="context-container"></div>

        <div class="form-group">
          <label for="issue-nl-input">Describe what you want to build or fix:</label>
          <textarea
            id="issue-nl-input"
            class="issue-nl-input"
            rows="6"
            placeholder="Example: Add dark mode toggle to the settings page with persistent user preference..."
          ></textarea>
          <div class="char-count" id="issue-char-count">0 / 5000 characters</div>
        </div>

        <div id="issue-error" class="error-message" style="display: none;"></div>

        <div class="button-group">
          <button id="generate-issue-btn" class="btn btn-primary">Generate Issue</button>
          <button id="clear-issue-btn" class="btn btn-secondary">Clear</button>
        </div>

        <div id="issue-preview-section" style="display: none;">
          <h3>Issue Preview</h3>
          <div id="issue-metadata" class="issue-metadata"></div>
          <div id="issue-preview-content" class="issue-preview-content">
            <pre id="issue-preview-text"></pre>
          </div>
          <div id="issue-requirements" class="requirements-section" style="display: none;">
            <h4>Extracted Requirements</h4>
            <ul id="requirements-list"></ul>
          </div>
          <div id="issue-estimation" class="estimation"></div>
          <div class="button-group">
            <button id="post-issue-btn" class="btn btn-primary">Post to GitHub</button>
            <button id="edit-issue-btn" class="btn btn-secondary">Edit</button>
          </div>
        </div>

        <div id="issue-success" class="success-message" style="display: none;">
          <span class="success-icon">✓</span>
          <span id="issue-success-text"></span>
        </div>
      </div>
    `;

    this.attachEventListeners();
    this.updateGitHubStatus();
    this.updateProjectContext();
  }

  private attachEventListeners(): void {
    const nlInput = document.getElementById('issue-nl-input') as HTMLTextAreaElement;
    const generateBtn = document.getElementById('generate-issue-btn') as HTMLButtonElement;
    const clearBtn = document.getElementById('clear-issue-btn') as HTMLButtonElement;
    const charCount = document.getElementById('issue-char-count') as HTMLElement;

    // Input handling
    nlInput?.addEventListener('input', (e) => {
      const target = e.target as HTMLTextAreaElement;
      this.nlInput = target.value;
      charCount.textContent = `${target.value.length} / 5000 characters`;
      this.hideError();
    });

    // Generate button
    generateBtn?.addEventListener('click', () => this.handleGenerateIssue());

    // Clear button
    clearBtn?.addEventListener('click', () => this.handleClear());

    // Allow Cmd+Enter or Ctrl+Enter to generate
    nlInput?.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        this.handleGenerateIssue();
      }
    });
  }

  private async handleGenerateIssue(): Promise<void> {
    // Validate input
    const validation = validateNLInput(this.nlInput);
    if (!validation.isValid) {
      this.showError(validation.error || 'Invalid input');
      return;
    }

    const generateBtn = document.getElementById('generate-issue-btn') as HTMLButtonElement;
    const nlInput = document.getElementById('issue-nl-input') as HTMLTextAreaElement;

    // Disable inputs
    generateBtn.disabled = true;
    nlInput.disabled = true;
    generateBtn.innerHTML = '<span class="loading"></span> Processing...';

    try {
      const request: NLProcessingRequest = {
        nl_input: this.nlInput,
        project_path: '.',
        auto_detect_context: true,
        confirm_before_post: true,
      };

      this.processingResponse = await processNaturalLanguage(request);

      if (this.processingResponse.error) {
        throw new Error(this.processingResponse.error);
      }

      // Generate preview
      const previewRequest: IssuePreviewRequest = {
        issue: this.processingResponse.issue,
        format: 'markdown',
      };
      const previewResponse = await previewIssue(previewRequest);
      this.issuePreview = previewResponse.formatted_preview;

      // Update project context if returned
      if (this.processingResponse.project_context) {
        this.projectContext = this.processingResponse.project_context;
        this.updateProjectContext();
      }

      // Display preview
      this.displayIssuePreview();
    } catch (error) {
      this.showError(error instanceof Error ? error.message : 'Failed to process request');
    } finally {
      generateBtn.disabled = false;
      nlInput.disabled = false;
      generateBtn.innerHTML = 'Generate Issue';
    }
  }

  private displayIssuePreview(): void {
    if (!this.processingResponse) return;

    const previewSection = document.getElementById('issue-preview-section');
    const metadataEl = document.getElementById('issue-metadata');
    const previewText = document.getElementById('issue-preview-text');
    const requirementsSection = document.getElementById('issue-requirements');
    const requirementsList = document.getElementById('requirements-list');
    const estimationEl = document.getElementById('issue-estimation');

    if (previewSection) previewSection.style.display = 'block';

    // Display metadata
    if (metadataEl) {
      const issue = this.processingResponse.issue;
      metadataEl.innerHTML = `
        <span class="issue-type" style="background-color: ${getIssueTypeColor(issue.classification)}">
          ${issue.classification}
        </span>
        <span class="workflow-badge">
          ${issue.workflow} (${issue.model_set})
        </span>
        <span class="confidence-score">
          Confidence: ${(this.processingResponse.confidence_score * 100).toFixed(0)}%
        </span>
      `;
    }

    // Display preview content
    if (previewText) {
      previewText.textContent = this.issuePreview;
    }

    // Display requirements
    if (this.processingResponse.requirements.length > 0 && requirementsSection && requirementsList) {
      requirementsSection.style.display = 'block';
      requirementsList.innerHTML = this.processingResponse.requirements
        .slice(0, 5)
        .map(req => `<li>${req}</li>`)
        .join('');
    }

    // Display estimation
    if (estimationEl && this.projectContext) {
      estimationEl.innerHTML = `
        <span class="estimation-label">Estimated Time:</span>
        <span class="estimation-value">${estimateTimeFromComplexity(this.projectContext.complexity)}</span>
      `;
    }

    // Attach event listeners for preview actions
    const postBtn = document.getElementById('post-issue-btn');
    const editBtn = document.getElementById('edit-issue-btn');

    postBtn?.addEventListener('click', () => this.handlePostIssue());
    editBtn?.addEventListener('click', () => this.handleEditIssue());
  }

  private async handlePostIssue(): Promise<void> {
    if (!this.processingResponse) return;

    const postBtn = document.getElementById('post-issue-btn') as HTMLButtonElement;
    postBtn.disabled = true;
    postBtn.innerHTML = '<span class="loading"></span> Posting...';

    try {
      const request: GitHubPostRequest = {
        issue: this.processingResponse.issue,
        dry_run: false,
      };

      const response = await postIssueToGitHub(request);

      if (response.success && response.issue_number) {
        this.showSuccess(response.issue_number, response.issue_url);
      } else {
        throw new Error(response.error || 'Failed to post issue');
      }
    } catch (error) {
      this.showError(error instanceof Error ? error.message : 'Failed to post issue');
    } finally {
      postBtn.disabled = false;
      postBtn.innerHTML = 'Post to GitHub';
    }
  }

  private handleEditIssue(): void {
    const previewSection = document.getElementById('issue-preview-section');
    const nlInput = document.getElementById('issue-nl-input') as HTMLTextAreaElement;

    if (previewSection) previewSection.style.display = 'none';
    if (nlInput) {
      nlInput.focus();
      nlInput.scrollIntoView({ behavior: 'smooth' });
    }
  }

  private handleClear(): void {
    const nlInput = document.getElementById('issue-nl-input') as HTMLTextAreaElement;
    const previewSection = document.getElementById('issue-preview-section');
    const successEl = document.getElementById('issue-success');
    const charCount = document.getElementById('issue-char-count');

    this.nlInput = '';
    this.processingResponse = null;
    this.issuePreview = '';

    if (nlInput) nlInput.value = '';
    if (previewSection) previewSection.style.display = 'none';
    if (successEl) successEl.style.display = 'none';
    if (charCount) charCount.textContent = '0 / 5000 characters';
    this.hideError();
  }

  private updateGitHubStatus(): void {
    const statusEl = document.getElementById('gh-status');
    if (!statusEl || !this.ghStatus) return;

    statusEl.innerHTML = `
      <div class="github-status">
        <div class="status-item">
          <span class="status-label">GitHub CLI:</span>
          <span class="status-value ${this.ghStatus.installed ? 'success' : 'error'}">
            ${this.ghStatus.installed ? '✓ Installed' : '✗ Not Installed'}
          </span>
        </div>
        ${this.ghStatus.installed ? `
          <div class="status-item">
            <span class="status-label">Authentication:</span>
            <span class="status-value ${this.ghStatus.authenticated ? 'success' : 'error'}">
              ${this.ghStatus.authenticated ? `✓ ${this.ghStatus.user}` : '✗ Not Authenticated'}
            </span>
          </div>
        ` : ''}
      </div>
    `;

    if (!this.ghStatus.authenticated) {
      statusEl.innerHTML += `
        <div class="warning-message">
          ⚠ Run <code>gh auth login</code> to authenticate GitHub CLI
        </div>
      `;
    }
  }

  private updateProjectContext(): void {
    const contextEl = document.getElementById('project-context');
    if (!contextEl || !this.projectContext) return;

    contextEl.innerHTML = `
      <div class="project-context">
        <h4>Project Context</h4>
        <div class="context-grid">
          <div class="context-item">
            <span class="context-label">Type:</span>
            <span class="context-value">
              ${this.projectContext.is_new_project ? 'New Project' : 'Existing Codebase'}
            </span>
          </div>
          ${this.projectContext.framework ? `
            <div class="context-item">
              <span class="context-label">Framework:</span>
              <span class="context-value">${this.projectContext.framework}</span>
            </div>
          ` : ''}
          ${this.projectContext.backend ? `
            <div class="context-item">
              <span class="context-label">Backend:</span>
              <span class="context-value">${this.projectContext.backend}</span>
            </div>
          ` : ''}
          <div class="context-item">
            <span class="context-label">Complexity:</span>
            <span class="context-value complexity-${this.projectContext.complexity}">
              ${this.projectContext.complexity}
            </span>
          </div>
        </div>
      </div>
    `;
  }

  private showError(message: string): void {
    const errorEl = document.getElementById('issue-error');
    if (errorEl) {
      errorEl.textContent = message;
      errorEl.style.display = 'block';
    }
  }

  private hideError(): void {
    const errorEl = document.getElementById('issue-error');
    if (errorEl) {
      errorEl.style.display = 'none';
    }
  }

  private showSuccess(issueNumber: number, issueUrl?: string): void {
    const successEl = document.getElementById('issue-success');
    const successText = document.getElementById('issue-success-text');
    const previewSection = document.getElementById('issue-preview-section');

    if (successEl && successText) {
      successText.innerHTML = `
        Issue #${issueNumber} created successfully!
        ${issueUrl ? `<a href="${issueUrl}" target="_blank" rel="noopener noreferrer">View on GitHub →</a>` : ''}
      `;
      successEl.style.display = 'block';
    }

    if (previewSection) {
      previewSection.style.display = 'none';
    }

    // Clear form after success
    setTimeout(() => {
      this.handleClear();
    }, 5000);
  }
}