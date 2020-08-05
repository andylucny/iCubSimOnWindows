if exist shape_predictor_68_face_landmarks.dat (
    echo "face landmark detector already downloaded"
) else (
    echo "downloading face landmark detector, please wait"
    bitsadmin /transfer myDownload /download "http://www.robotika.sk/seminar/2020/shape_predictor_68_face_landmarks.dat" %cd%\shape_predictor_68_face_landmarks.dat
)
@set PATH=.;iCubSim\bin;%PATH%
python example_imitation.py
pause
