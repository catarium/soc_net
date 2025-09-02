import "./Post.css";

export default function Post({ title, author, text, images, profilePicture, authorId}) {
  return (
    <>
      <div className="Post">
        <div className="PostHeader">
          <div className="PostTitle">{title}</div>
          <div className="PostAuthorBlock">
            <img className="MiniProfilePicture" src={"/static/images/" + profilePicture}></img>
            <a href={"/profile/" + authorId} className="PostAuthorName">{author}</a>
          </div>
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
