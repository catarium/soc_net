
import "./SubPosts.css";
import Footer from "../Footer/Footer.jsx";
import Header from "../Header/Header.jsx";
import { useEffect, useState, useRef } from "react";
import PostsList from "../PostsList/PostsList.jsx";
import PostForm from "../PostForm/PostForm.jsx";

export default function SubPosts() {
  const [postData, setPostData] = useState([]);
  const [userData, setUserData] = useState(null);

  // refs to avoid stale closures
  const userDataRef = useRef(null);
  const loadingRef = useRef(false);
  const offsetsRef = useRef({}); // per-creator offsets
  const exhaustedRef = useRef(false);
  const flag = useRef(false);
  const limit = 10;

  // keep ref in sync with state
  useEffect(() => {
    userDataRef.current = userData;
  }, [userData]);

  // fetch current user on mount
  useEffect(() => {
    async function f() {
      const res = await fetch(`/api/auth/me`);
      if (!res.ok) {
        alert(await res.text());
        return;
      }
      setUserData((await res.json()).res);
    }
    f();
  }, []);

  // initialize offsets and load first page when userData arrives
  useEffect(() => {
    if (!userData) return;

    // reset state for fresh subscription list
    setPostData([]);
    offsetsRef.current = {};
    exhaustedRef.current = false;
    flag.current = false;

    userData.subscriptions.forEach((sub) => {
      offsetsRef.current[sub.id] = 0;
    });

    // load first page
    loadMorePosts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userData]);

  // scroll listener (mounted once) — uses refs inside loadMorePosts so it's safe
  useEffect(() => {
    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
      if (scrollTop === 0 || flag.current) return;
      if (scrollTop + clientHeight >= scrollHeight - 50) {
        if (!loadingRef.current && !exhaustedRef.current) {
          loadMorePosts();
        }
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []); // mount once

  // main loader — reads from refs so it's safe from stale closures
  async function loadMorePosts() {
    const curUser = userDataRef.current;
    if (!curUser || loadingRef.current || exhaustedRef.current) return;

    const subs = curUser.subscriptions || [];
    if (subs.length === 0) {
      exhaustedRef.current = true;
      return;
    }

    loadingRef.current = true;
    try {
      const fetchPromises = subs.map((sub) => {
        const offset = offsetsRef.current[sub.id] || 0;
        return fetch(`/api/userapi/post/?creator_id=${sub.id}&offset=${offset}&limit=${limit}`)
          .then(async (res) => {
            if (!res.ok) {
              console.error(`Failed to fetch posts for creator ${sub.id}`, await res.text());
              return [];
            }
            const json = await res.json();
            return json.res || [];
          })
          .catch((err) => {
            console.error("fetch error for creator", sub.id, err);
            return [];
          });
      });

      const results = await Promise.all(fetchPromises);
      const newPosts = results.flat();

      // update offsets per creator
      subs.forEach((sub, idx) => {
        const got = results[idx]?.length || 0;
        offsetsRef.current[sub.id] = (offsetsRef.current[sub.id] || 0) + got;
      });

      // append and dedupe by id (optional but helpful)
      setPostData((prev) => {
        const map = new Map();
        prev.concat(newPosts).forEach((p) => {
          if (p && p.id !== undefined) {
            map.set(p.id, p);
          } else {
            // if no id, just append (give unique key)
            map.set(Symbol(), p);
          }
        });
        return Array.from(map.values());
      });

      // if every subscription returned 0 items, mark exhausted
      const allEmpty = results.every((arr) => !arr || arr.length === 0);
      if (allEmpty) {
        exhaustedRef.current = true;
        flag.current = true;
      } else {
        exhaustedRef.current = false;
      }
    } finally {
      loadingRef.current = false;
    }
  }

  return (
    <>
      {<Header />}
      <div className="Content">
        {<PostForm />}
        {<PostsList data={postData} />}
      </div>
      {<Footer SectionName="Subs" />}
    </>
  );
}

