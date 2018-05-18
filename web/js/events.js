// Navbar click events
$("#MainLogoLinkBtn").click(function() {
	Index.switchBlock("Main");
});
$("#GoToAnalyzeBtn").click(function() {
	Index.switchBlock("AnalyzeType");
});
$("#GoToUtilsBtn").click(function() {
	Index.switchBlock("Utils");
});
$("#GoToHelpBtn").click(function() {
	Index.switchBlock("Help");
});
$("#GoToAboutBtn").click(function() {
	Index.switchBlock("About");
});

// Main block click events
$("#TryAnalyzeBtn").click(function() {
	Index.switchBlock("AnalyzeType");
});

// Analyze type block click events
$("#GoToUploadBtn").click(function() {
	Index.switchBlock("AnalyzeSystem");
});

// Analyze system block click events
$("#StartAnalyzeSystemBtn").click(function() {
	$("#ProcessingText").html("Загрузка данных...");
	Index.switchBlock("Processing");
	API.baseDataAnalyze();
});