import "./AllPosts.css";
import Footer from "../Footer/Footer.jsx";
import Header from "../Header/Header.jsx";
import { useEffect, useState, useRef } from "react";
import PostsList from "../PostsList/PostsList.jsx";
import PostForm from "../PostForm/PostForm.jsx";

export default function AllPosts() {
    const [data, setData] = useState([]);
    const [offset, setOffset] = useState(0);
    const [isAtBottom, setIsAtBottom] = useState(false);
    const limit = 10;
    const flag = useRef(false);

    const handleScroll = () => {
        const { scrollTop, scrollHeight, clientHeight } =
            document.documentElement;

        console.log(flag)
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
            const res = await fetch(`/api/userapi/post/?offset=${offset}`);

            if (!res.ok) {
                alert(res.text());
            }
            const postsData = (await res.json()).res
            setData(data.concat(postsData));
            if (postsData.length == 0) {
                flag.current = true;
            } else {
                flag.current = false;
            }
            console.log(flag)
        }
        f();
    }, [offset]);
    return (
        <>
            {<Header />}
            <div className="Content">
                {<PostForm />}
                {<PostsList data={data} />}
            </div>
            {<Footer SectionName="All" />}
        </>
    );
}
