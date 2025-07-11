import {Composition, staticFile} from 'remotion';
import {
	CaptionedVideo,
	calculateCaptionedVideoMetadata,
	captionedVideoSchema,
} from './CaptionedVideo';
import {LayeredVideo, layeredVideoSchema} from './LayeredVideo';
import VideoInfo from '../public/info.json';
import {RepostVideo} from './RepostVideo';

// Each <Composition> is an entry in the sidebar!

export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Composition
				id="CaptionedVideo"
				component={CaptionedVideo}
				calculateMetadata={calculateCaptionedVideoMetadata}
				schema={captionedVideoSchema}
				width={1080}
				height={1920}
				defaultProps={{
					src: staticFile('temp.mp4'),
				}}
			/>

			<Composition
				id="LayeredVideo"
				component={LayeredVideo}
				fps={30}
				durationInFrames={Math.floor(VideoInfo.duration_in_seconds * 30)}
				schema={layeredVideoSchema}
				width={1080}
				height={1920}
				defaultProps={{
					backgroundSource: staticFile('gameplay.mp4'),
				}}
			/>

			<Composition
				id="RepostVideo"
				component={RepostVideo}
				fps={30}
				durationInFrames={Math.floor(VideoInfo.duration_in_seconds * 30)}
				width={1080}
				height={1920}
			/>
		</>
	);
};
