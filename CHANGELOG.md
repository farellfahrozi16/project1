# Changelog

All notable changes to the KURO Performance Postural Assessment project will be documented in this file.

## [1.0.0] - 2025-01-07

### Added
- Initial release of KURO Performance Postural Assessment System
- Dashboard 1: Welcome screen with user data input (name and height)
- Dashboard 2: Main menu with image upload, model upload, and analysis controls
- Dashboard 3: Before/After visualization with analysis comparison
- Dashboard 4: Detailed report with graphs, tables, and CSV export
- YOLO integration for posture detection and classification
- Support for 4 main posture classifications: Normal, Kyphosis, Lordosis, Swayback
- Keypoint detection for 17 body points
- Two analysis types: Back/Front Analysis and Side Analysis
- Posture calculation engine with metrics:
  - Shoulder Imbalance
  - Hip Imbalance
  - Spine Deviation
  - Head Shift
  - Head Tilt
  - Overall Posture Score (0-100)
- Visualization charts for analysis results
- CSV export functionality for reports
- Supabase database integration for data persistence
- Comprehensive documentation (README.md, INTEGRATION_GUIDE.md)
- Automated head alignment for realistic imbalance values
- Confidence threshold adjustment with slider
- Single and batch image analysis modes
- System info display
- Modern GUI with KURO Performance branding

### Features
- Real-time image preview
- Confidence level classification (Sangat Tinggi, Tinggi, Sedang, Rendah, Sangat Rendah)
- Automatic analysis type determination based on classification
- Pixel-to-millimeter ratio calculation for accurate measurements
- Bounding box and keypoint visualization
- Detailed keypoint information with emoji indicators
- Recommendation system based on posture score
- Background processing for better UX

### Technical
- Built with Python and Tkinter for GUI
- Ultralytics YOLO for object detection
- OpenCV for image processing
- Matplotlib for visualization
- Pandas for data handling
- Supabase for cloud database
- Modular architecture for easy maintenance

### Database Schema
- `user_sessions` table for storing user information
- `analysis_results` table for storing analysis data
- Row Level Security (RLS) policies for data protection

### Documentation
- Complete README with installation and usage instructions
- Integration guide for web deployment
- Code comments and docstrings
- Troubleshooting section

## [Unreleased]

### Planned Features
- Multi-language support (English, Indonesian)
- Export to PDF with detailed report
- Historical analysis tracking
- Comparison between multiple sessions
- Exercise recommendations based on posture type
- Video analysis support
- Mobile app version
- Cloud-based model hosting
- Real-time collaboration features
- Advanced statistics and trends
