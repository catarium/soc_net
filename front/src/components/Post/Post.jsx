import "./Post.css";

export default function Post({ title, author, text, images }) {
    return (
        <>
            <div className="Post">
                <div className="PostHeader">
                    <div className="PostTitle">{title}</div>
                    <div className="PostAuthor">{author}</div>
                </div>
                <div className="PostContent">
                    <div className="PosText">{text}</div>
                    {images.map((item) => (
                        <div className="PostImage">
                            <img src={`/static/images/` + item} />
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
