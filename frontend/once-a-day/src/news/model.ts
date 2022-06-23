
export interface InternetContent {
	url: string;
	timestamp: number;
	location: string;
	title: string;
	description: string;
	mainCategory: string;
	upvotes: number;
	comments: number;
	imageSourceURL: string;
} 

export function getInternetContentFilterKey(content: InternetContent): string {
	if (!content.mainCategory) {
		return content.location
	}

	let subkey = content.mainCategory.split("-").map(capitaliseWord).join(" ")
	return `${content.location} - ${subkey}`
}

export function capitaliseWord(word: string): string {
	return word[0].toUpperCase() + word.substring(1)
}