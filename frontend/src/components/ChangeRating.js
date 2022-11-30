export default function ChangeRating(props) {
    return (
      <input
        type="number"
        step="1"
        min="0"
        max="5"
        value={props.rating}
        onChange={(e) => {
          if (e.target.value > 5)
            return alert("Números del 1 al 5 :)");
          return props.handleRating(e.target.value);
        }}
      />
    );
  }
  