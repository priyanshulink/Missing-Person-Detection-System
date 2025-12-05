/**
 * Reports Module
 */

class ReportsManager {
    constructor() {
        this.reports = [];
    }

    init() {
        this.loadReports();
        
        // Refresh reports every 30 seconds
        setInterval(() => this.loadReports(), 30000);
    }

    async loadReports() {
        try {
            const data = await api.getReports({ limit: 50 });
            this.reports = data.reports || [];
            this.renderReports();
        } catch (error) {
            console.error('Error loading reports:', error);
            document.getElementById('reportsList').innerHTML = 
                '<p class="no-data">Error loading reports</p>';
        }
    }

    renderReports() {
        const reportsList = document.getElementById('reportsList');
        
        if (!this.reports || this.reports.length === 0) {
            reportsList.innerHTML = '<p class="no-data">No reports found</p>';
            return;
        }

        reportsList.innerHTML = this.reports.map(report => {
            const cameraName = report.camera?.name || report.detectionInfo?.cameraName || 'Unknown Camera';
            const cameraLocation = report.camera?.location || report.detectionInfo?.cameraLocation || 'Unknown Location';
            const personStatus = report.person?.status || 'missing';
            
            return `
            <div class="report-item">
                <div class="report-info">
                    <h4>
                        ${report.person?.name || 'Unknown Person'}
                        ${personStatus === 'found' ? '<span class="badge found" style="margin-left: 10px; background: #10b981; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.75em;">FOUND ✅</span>' : ''}
                    </h4>
                    <div class="report-meta">
                        <div>
                            <i class="fas fa-video"></i> <strong>${cameraName}</strong>
                        </div>
                        <div style="margin-top: 5px;">
                            <i class="fas fa-map-marker-alt"></i> ${cameraLocation}
                        </div>
                        <div style="margin-top: 5px;">
                            <i class="fas fa-clock"></i> ${this.formatDate(report.detectionInfo?.timestamp)}
                        </div>
                        <div style="margin-top: 5px;">
                            <i class="fas fa-check-circle"></i> Status: <span class="status-badge status-${report.verificationStatus}">${report.verificationStatus}</span>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="similarity-badge">
                        ${(report.matchDetails?.similarity * 100).toFixed(1)}% Match
                    </div>
                    <div style="margin-top: 10px;">
                        ${this.getVerificationButtons(report)}
                    </div>
                </div>
            </div>
        `}).join('');
    }

    getVerificationButtons(report) {
        if (report.verificationStatus === 'pending') {
            return `
                <button class="btn btn-primary btn-small" onclick="reportsManager.verifyReport('${report._id}', '${report.person?._id}', 'confirmed')">
                    <i class="fas fa-check"></i> Confirm
                </button>
                <button class="btn btn-secondary btn-small" onclick="reportsManager.verifyReport('${report._id}', '${report.person?._id}', 'false_positive')">
                    <i class="fas fa-times"></i> False Positive
                </button>
            `;
        }
        return `<span style="color: var(--text-secondary);">Verified</span>`;
    }

    async verifyReport(reportId, personId, status) {
        try {
            // Update report verification status
            await api.verifyReport(reportId, status);
            
            // If confirmed, update person status to "found"
            if (status === 'confirmed' && personId) {
                await api.updatePersonStatus(personId, 'found');
            }
            
            this.loadReports();
            alert(status === 'confirmed' ? 'Report confirmed - Person marked as FOUND ✅' : 'Report marked as false positive');
        } catch (error) {
            console.error('Error verifying report:', error);
            alert('Error updating verification: ' + error.message);
        }
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString();
    }
}

// Create global instance
const reportsManager = new ReportsManager();
