import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import CajaComentarios from "./CajaComentarios";

const Modular = () => {
  const location = useLocation();
  const [subject, setSubject] = useState();
  const subjectRowData = location.state.rowData;

  /*useEffect(() => {
      const fetchSubject = async () => {
        try {
          let degree_code = subjectRowData.degree_code;
          let cve = subjectRowData.CVE
          let url = `http://192.9.147.109/subject/${degree_code}/${cve}`;
          let response = await fetch(url);
          let data = await response.json();
          setSubject(data);
        } catch (error) {
          alert("Ha ocurrido un error al solicitar los datos");
        }
      };
      fetchSubject();
  }, []);
*/

  console.log(subjectRowData)

  return (
    <div className="Fondo">
      <div className="Relleno"/>
      <div className="Body">
        <h1>Modular {subjectRowData.degree_code}</h1>
        <div>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. In convallis lacus in leo iaculis, a luctus nunc mollis. Aliquam lorem eros, eleifend vel condimentum sit amet, condimentum vitae dui. Fusce convallis diam ut tellus bibendum molestie. Cras sodales suscipit ex sit amet euismod. Duis id sem quis lorem iaculis tincidunt nec non velit. Phasellus eu tellus dignissim, tincidunt lectus sed, dignissim lorem. Duis sit amet commodo libero. Fusce sodales luctus lectus, ac elementum arcu maximus at.Aenean volutpat lorem leo, eget facilisis nunc sagittis iaculis. Mauris dictum et ex in accumsan. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nam nec lacus dignissim, viverra dui et, venenatis purus. Nunc congue porttitor suscipit. Phasellus sit amet sollicitudin orci. Nullam vel est porttitor, dapibus orci in, vulputate erat. Ut a pharetra urna. Etiam finibus pretium dolor et lacinia. Nulla ut tortor urna.
          Sed consequat sem ipsum, sit amet commodo nibh euismod in. Quisque viverra tortor volutpat nisi iaculis commodo. Etiam mattis ante velit, ac tristique urna pretium vitae. Cras interdum purus eget cursus accumsan. Ut venenatis libero sed orci pretium malesuada. Morbi at est fringilla, fermentum sem et, tempus mauris. Morbi rhoncus, lacus id commodo rhoncus, eros magna condimentum nunc, vel semper est justo sed ligula. Morbi rhoncus accumsan rhoncus. Duis libero massa, dignissim id justo at, tincidunt finibus leo. Vivamus pellentesque, metus nec molestie aliquet, purus purus accumsan felis, ac sagittis eros mauris ut lacus. Nullam semper libero in ligula fringilla accumsan.Vestibulum mattis erat eu tincidunt consequat. Suspendisse blandit metus eu nunc bibendum, ut dictum odio commodo. Donec augue nulla, varius eget ligula id, tempus interdum metus. Phasellus vel sem gravida, varius mauris a, ullamcorper nisl. Nullam sit amet fermentum nibh, a condimentum neque. Vestibulum a interdum leo. Nullam vel orci scelerisque, interdum purus sit amet, vulputate sapien. Phasellus posuere nibh at velit condimentum, quis venenatis magna posuere. Quisque tempus augue et gravida laoreet. Vivamus eu dui sed eros lacinia faucibus at quis leo. Cras auctor, mi ac pulvinar feugiat, metus nisl mattis quam, efficitur tristique ante est a erat. Fusce mi purus, ornare id luctus id, imperdiet id metus. Nunc finibus tortor id interdum rhoncus. Aliquam ut mauris pellentesque, aliquam purus gravida, cursus arcu. Integer scelerisque dolor malesuada, fringilla leo non, sollicitudin orci.Proin ac magna volutpat, accumsan nisi suscipit, fringilla diam. Aenean maximus, quam ut ultricies dapibus, nibh augue maximus sem, hendrerit sodales elit nisl sodales ipsum. Nullam tristique orci in lacus consectetur, pharetra viverra erat congue. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas id tristique tortor. Fusce sollicitudin a ante quis imperdiet. Praesent facilisis ante arcu, sit amet euismod erat efficitur in.
        </div>
        <a href={subjectRowData.modular_project_description}>Proyecto Modular INCO.pdf</a>.
        <div className="Relleno"/>
        <CajaComentarios subjectRowData={subjectRowData} />
      </div>
      <div className="Relleno"/>
    </div>
  );
  
}

export default Modular;