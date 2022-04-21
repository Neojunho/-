using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class LookatAudience : MonoBehaviour
{
    private float startTime; //프레젠테이션 시작 타임
    private float endTime; //프레젠테이션 종료 타임
    private float totalTime; //전체 프레젠테이션 타임
    public Transform m_tr;
    public float distance = 50.0f; //Ray의 길이
    public RaycastHit hit; //Raycasting 충돌 감지
    [SerializeField] private LayerMask m_layerMask; //충돌 정보    
    public RaycastHit[] hits; //충돌 정보를 여러개 담을 레이케스트 히트 배열
    [SerializeField] private GameObject focusingPoint;
    private float createTime = 0.1f;
    private float currentCreateTime = 0;
    private GameObject instantiateObj;
    private float destroyTime = 0.07f;
    bool focusDetector;
    string path;
    StreamWriter writer;
    bool settingFocuseDetector;
    bool closeFocuseDetector;
    System.DateTime nowTime = System.DateTime.Now;

    void Start()
    {
        m_tr = GetComponent<Transform>();
        string strDateTime = nowTime.ToString("yyyy/MM/dd hh/mm/ss");
        print(strDateTime);
        focusDetector = false;
        closeFocuseDetector = false;
        settingFocuseDetector = false;
        path = "Assets/Resources/" + strDateTime + ".txt";
        PresentationMissionScript.OnFocusingStart += settingDetector;
    }

    void FixedUpdate()
    {
        if(settingFocuseDetector)
        {
            if (!focusDetector)
            {
                focusDetector = true;
                settingFocuseDetector = false;
                writer = new StreamWriter(path, true);
                string strNowDateTime = 
                    nowTime.ToString("yyyy/MM/dd hh:mm:ss");
                writer.WriteLine(strNowDateTime);
                startTime = Time.time;
            }
        }
        if (focusDetector)
        {
            if(closeFocuseDetector)
            {
                focusDetector = false;
                closeFocuseDetector = false;
                endTime = Time.time;
                totalTime = endTime - startTime;

                writer.WriteLine("총 발표시간: " + totalTime);
                writer.Close();
            }
            currentCreateTime += Time.deltaTime;
            if (currentCreateTime >= createTime)
            {
                currentCreateTime = 0f;
                Ray ray = new Ray();
                ray.origin = m_tr.position; //Ray 시작점
                ray.direction = m_tr.forward; //Ray 방향
                if (Physics.Raycast(ray, out hit, distance, m_layerMask))
                {
                    instantiateObj = (GameObject)Instantiate(focusingPoint,
                    hit.transform.position, Quaternion.LookRotation(hit.point));
                    Destroy(instantiateObj, destroyTime);
                }
            }
            OnDrawRayLine();
        }
    }
    private void OnApplicationQuit()
    {
        writer.Close();
    }
    public void OnDrawRayLine()
    {
        if (hit.collider != null)
        {
            Debug.DrawLine(m_tr.position, m_tr.position + m_tr.forward * hit.distance, Color.red);
        }
        else
        {
            Debug.DrawLine(m_tr.position, m_tr.position + m_tr.forward * this.distance, Color.white);
        }
    }
    public void settingDetector(int value)
    {
        if(value == 1)
        {
            settingFocuseDetector = true;
        }else if(value == 2)
        {
            closeFocuseDetector = true;
        }
    }
}