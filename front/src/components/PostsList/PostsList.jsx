import './PostsList.css'
import Post from '../Post/Post.jsx';

export default function PostsList({data}) {
    return (
        <div className="PostsList">
            {data.map(
                (item) => (
                    <Post
                        title={item.name}
                        author={item.creator.name}
                        text={item.text}
                        images={item.media.map((media) => media.filename)}
                    />
                ),
            )}
        </div>
    );
}
