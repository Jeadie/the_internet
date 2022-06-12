
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
	const subkey = content.mainCategory != "" ? ` - ${content.mainCategory}` : ""
	return `${content.location}${subkey}`
}