/**
 * Dashboard Module
 */

class DashboardManager {
    constructor() {
        this.stats = null;
    }

    async init() {
        if (!authManager.isAuthenticated()) {
            return;
        }

        await this.loadStats();
        await this.loadRecentMatches();
        
        // Refresh stats every 30 seconds
        setInterval(() => this.loadStats(), 30000);
    }

    async loadStats() {
        try {
            // Get persons count
            const personsData = await api.getPersons({ limit: 1 });
            document.getElementById('totalPersons').textContent = personsData.total || 0;

            // Get reports stats
            const stats = await api.getReportStats();
            document.getElementById('totalMatches').textContent = stats.totalReports || 0;
            document.getElementById('pendingReports').textContent = stats.pendingReports || 0;
            
            // Critical alerts (confirmed reports)
            document.getElementById('criticalAlerts').textContent = stats.confirmedReports || 0;

            this.stats = stats;
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async loadRecentMatches() {
        try {
            const data = await api.getReports({ limit: 5 });
            const matchesList = document.getElementById('recentMatches');
            
            if (!data.reports || data.reports.length === 0) {
                matchesList.innerHTML = '<p class="no-data">No recent matches</p>';
                return;
            }

            matchesList.innerHTML = data.reports.map(report => {
                const cameraName = report.camera?.name || report.detectionInfo?.cameraName || 'Unknown Camera';
                const cameraLocation = report.camera?.location || report.detectionInfo?.cameraLocation || '';
                
                return `
                <div class="match-item">
                    <div>
                        <strong>${report.person?.name || 'Unknown'}</strong>
                        <div class="report-meta">
                            <i class="fas fa-video"></i> <strong>${cameraName}</strong>
                            ${cameraLocation ? `<br><i class="fas fa-map-marker-alt"></i> ${cameraLocation}` : ''}
                            <span style="margin-left: 15px;">
                                <i class="fas fa-clock"></i> ${this.formatDate(report.detectionInfo?.timestamp)}
                            </span>
                        </div>
                    </div>
                    <div class="similarity-badge">
                        ${(report.matchDetails?.similarity * 100).toFixed(1)}%
                    </div>
                </div>
            `}).join('');
        } catch (error) {
            console.error('Error loading recent matches:', error);
        }
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString();
    }
}

// Create global instance
const dashboardManager = new DashboardManager();
