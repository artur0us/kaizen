var Index = {
	hideAllBlocks: function() {
		$("#MainBlock").css('display', 'none');
		$("#AnalyzeTypeBlock").css('display', 'none');
		$("#AnalyzeSystemBlock").css('display', 'none');
		$("#AnalyzeSystemResultBlock").css('display', 'none');
		$("#UtilsBlock").css('display', 'none');
		$("#HelpBlock").css('display', 'none');
		$("#AboutBlock").css('display', 'none');
		$("#ProcessingBlock").css('display', 'none');
		$("#AnalyzeErrorBlock").css('display', 'none');
	},
	switchBlock: function(blockName) {
		this.hideAllBlocks();
		switch(blockName) {
			case "Main": {
				$("#MainBlock").css('display', 'block');
				break;
			};
			case "AnalyzeType": {
				$("#AnalyzeTypeBlock").css('display', 'block');
				break;
			};
			case "AnalyzeSystem": {
				$("#AnalyzeSystemBlock").css('display', 'block');
				break;
			};
			case "AnalyzeSystemResult": {
				$("#AnalyzeSystemResultBlock").css('display', 'block');
				break;
			};
			case "Utils": {
				$("#UtilsBlock").css('display', 'block');
				break;
			};
			case "Help": {
				$("#HelpBlock").css('display', 'block');
				break;
			};
			case "About": {
				$("#AboutBlock").css('display', 'block');
				break;
			};
			case "Processing": {
				$("#ProcessingBlock").css('display', 'block');
				break;
			};
			case "AnalyzeError": {
				$("#AnalyzeErrorBlock").css('display', 'block');
				break;
			};
			default: {
				break;
			};
		}
	},
}