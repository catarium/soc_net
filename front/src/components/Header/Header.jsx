import "./Header.css";

function Search() {
    return (
        <>
            <input
                className="SearchInput"
                type="text"
                placeholder="type here something..."
            />
        </>
    );
}

export default function Header() {
    return (
        <>
            <div className="Header">
                <div className="HeaderEl">
                    {<Search />}
                </div>
            </div>
        </>
    );
}
