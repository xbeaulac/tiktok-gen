import React from 'react';
import {
	AbsoluteFill,
	Img,
	Audio,
	OffthreadVideo,
	Series,
	useVideoConfig,
	staticFile,
} from 'remotion';
import {z} from 'zod';
import VideoInfo from '../../public/info.json';

export const layeredVideoSchema = z.object({
	backgroundSource: z.string(),
});

export const LayeredVideo: React.FC<z.infer<typeof layeredVideoSchema>> = ({
	backgroundSource,
}) => {
	const imagePaths = VideoInfo.image_paths;
	const audioPaths = VideoInfo.audio_paths;
	const {fps} = useVideoConfig();
	const mediaPath = (path: string) => {
		return staticFile(path.replace('public/', ''));
	};
	return (
		<AbsoluteFill>
			<AbsoluteFill>
				<OffthreadVideo src={backgroundSource} />
			</AbsoluteFill>
			<AbsoluteFill>
				<Series>
					{imagePaths.map((imagePath, index) => (
						<Series.Sequence
							key={imagePath}
							durationInFrames={VideoInfo.durations[index] * fps}
						>
							<AbsoluteFill
								style={{
									width: '100%',
									height: '75%',
									justifyContent: 'center',
								}}
							>
								<Img
									src={mediaPath(imagePath)}
									style={{
										width: '75%',
										height: 'fit-content',
										objectFit: 'contain',
										margin: '0 auto',
									}}
								/>
							</AbsoluteFill>
							<AbsoluteFill>
								<Audio src={mediaPath(audioPaths[index])} />
							</AbsoluteFill>
						</Series.Sequence>
					))}
				</Series>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
