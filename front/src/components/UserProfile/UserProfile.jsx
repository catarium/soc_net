import "./UserProfile.css";
import Footer from "../Footer/Footer.jsx";
import Header from "../Header/Header.jsx";
import { useEffect, useRef, useState } from "react";
import { useParams } from "react-router";
import PostsList from "../PostsList/PostsList.jsx";
import PostForm from "../PostForm/PostForm.jsx";

function UserCard({ ProfilePictureSrc, ProfileName }) {
  return (
    <>
      <div className="UserCard">
        <div className="ProfilePictureBlock">
          <img className="ProfilePicture" src={ProfilePictureSrc}></img>
        </div>

        <div className="ProfileNameBlock">
          {ProfileName}
        </div>
      </div>
    </>
  );
}

export default function UserProfile() {
  const [userData, setUserData] = useState(null);
  const [data, setData] = useState([]);
  const [offset, setOffset] = useState(0);
  const [isAtBottom, setIsAtBottom] = useState(false);
  const limit = 10;
  const flag = useRef(false);
  const { userId } = useParams();

  const handleScroll = () => {
    const { scrollTop, scrollHeight, clientHeight } =
      document.documentElement;

    console.log(flag);
    if ((scrollTop == 0) || (flag.current)) {
      return;
    }
    if (scrollTop + clientHeight >= scrollHeight - 50) { // Add a small buffer for precision
      setIsAtBottom(true);
    } else {
      setIsAtBottom(false);
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);

    // Cleanup the event listener on component unmount
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []); // Empty dependency array ensures the effect runs only once on mount

  useEffect(() => {
    if (isAtBottom) {
      // Execute your function here when the user reaches the bottom
      setOffset(offset + limit);
      // Example: loadMoreItems();
    }
  }, [isAtBottom]); // Rerun this effect when isAtBottom changes

  useEffect(() => {
    async function f() {
      const res = await fetch(`/api/userapi/user/${userId}`);
      if (!res.ok) {
        alert(await res.text());
        return;
      }
      setUserData((await res.json()).user);
    }
    f();
  }, []);

  useEffect(() => {
    async function f() {
      if (!userData) {
        return;
      }
      const res = await fetch(
        `/api/userapi/post/?offset=${offset}&creator_id=${userData.id}`,
      );

      if (!res.ok) {
        alert(res.text());
      }
      const postsData = (await res.json()).res;
      setData(data.concat(postsData));
      if (postsData.length == 0) {
        flag.current = true;
      } else {
        flag.current = false;
      }
      console.log(flag);
    }
    f();
  }, [offset, userData]);
  return (
    <>
      {<Header />}
      <div className="Content">
        {<UserCard ProfilePictureSrc={userData ? (userData.profile_picture ? "/static/images/" + userData.profile_picture.filename : "") : ""} ProfileName={userData ? userData.name : ""} />}
        {<PostForm />}
        {<PostsList data={data} />}
      </div>
      {<Footer SectionName="All" />}
    </>
  );
}
