/*=========================================================================
 *
 *  Copyright RTK Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/

#include "rtkfieldofview_ggo.h"
#include "rtkGgoFunctions.h"
#include "rtkThreeDCircularProjectionGeometryXMLFile.h"
#include "rtkRayEllipsoidIntersectionImageFilter.h"
#include "rtkFieldOfViewImageFilter.h"
#include "rtkConstantImageSource.h"
#include "rtkBackProjectionImageFilter.h"
#ifdef RTK_USE_CUDA
#  include "rtkCudaBackProjectionImageFilter.h"
#endif

#include <itkImageFileReader.h>
#include <itkImageFileWriter.h>
#include <itkThresholdImageFilter.h>
#include <itkDivideImageFilter.h>
#include <itkMaskImageFilter.h>

int main(int argc, char * argv[])
{
  GGO(rtkfieldofview, args_info);

  using OutputPixelType = float;
  constexpr unsigned int Dimension = 3;

  // Check on hardware parameter
#ifndef RTK_USE_CUDA
  if(!strcmp(args_info.hardware_arg, "cuda") )
    {
    std::cerr << "The program has not been compiled with cuda option" << std::endl;
    return EXIT_FAILURE;
    }
#endif

#ifdef RTK_USE_CUDA
  using OutputImageType = itk::CudaImage< OutputPixelType, Dimension >;
#else
  using OutputImageType = itk::Image< OutputPixelType, Dimension >;
#endif

  // Projections reader
  using ReaderType = rtk::ProjectionsReader< OutputImageType >;
  ReaderType::Pointer reader = ReaderType::New();
  rtk::SetProjectionsReaderFromGgo<ReaderType, args_info_rtkfieldofview>(reader, args_info);

  // Geometry
  if(args_info.verbose_flag)
    std::cout << "Reading geometry information from "
              << args_info.geometry_arg
              << "..."
              << std::endl;

  rtk::ThreeDCircularProjectionGeometryXMLFileReader::Pointer geometryReader;
  geometryReader = rtk::ThreeDCircularProjectionGeometryXMLFileReader::New();
  geometryReader->SetFilename(args_info.geometry_arg);
  TRY_AND_EXIT_ON_ITK_EXCEPTION( geometryReader->GenerateOutputInformation() )

  // Reconstruction reader
  using ImageReaderType = itk::ImageFileReader<  OutputImageType >;
  ImageReaderType::Pointer unmasked_reconstruction = ImageReaderType::New();
  unmasked_reconstruction->SetFileName(args_info.reconstruction_arg);

  if(!args_info.bp_flag)
    {
    // FOV filter
    using FOVFilterType = rtk::FieldOfViewImageFilter<OutputImageType, OutputImageType>;
    FOVFilterType::Pointer fieldofview=FOVFilterType::New();
    fieldofview->SetMask(args_info.mask_flag);
    fieldofview->SetInput(0, unmasked_reconstruction->GetOutput());
    fieldofview->SetProjectionsStack(reader->GetOutput());
    fieldofview->SetGeometry(geometryReader->GetOutputObject());
    fieldofview->SetDisplacedDetector(args_info.displaced_flag);
    TRY_AND_EXIT_ON_ITK_EXCEPTION( fieldofview->Update() )

    // Write
    using WriterType = itk::ImageFileWriter<  OutputImageType >;
    WriterType::Pointer writer = WriterType::New();
    writer->SetFileName( args_info.output_arg );
    writer->SetInput( fieldofview->GetOutput() );
    TRY_AND_EXIT_ON_ITK_EXCEPTION( writer->Update() )
    }
  else
    {
    if(args_info.displaced_flag)
      {
      std::cerr << "Options --displaced and --bp are not compatible (yet)." << std::endl;
      return EXIT_FAILURE;
      }

    TRY_AND_EXIT_ON_ITK_EXCEPTION( reader->UpdateOutputInformation() )
    TRY_AND_EXIT_ON_ITK_EXCEPTION( unmasked_reconstruction->UpdateOutputInformation() )

#ifdef RTK_USE_CUDA
    using MaskImgType = itk::CudaImage<float, 3>;
#else
    using MaskImgType = itk::Image<unsigned short, 3>;
#endif
    using ConstantType = rtk::ConstantImageSource<MaskImgType>;
    ConstantType::Pointer ones = ConstantType::New();
    ones->SetConstant(1);
    ones->SetInformationFromImage(reader->GetOutput());

    ConstantType::Pointer zeroVol = ConstantType::New();
    zeroVol->SetConstant(0.);
    zeroVol->SetInformationFromImage(unmasked_reconstruction->GetOutput());

    using BPType = rtk::BackProjectionImageFilter<MaskImgType, MaskImgType>;
    BPType::Pointer bp = BPType::New();
#ifdef RTK_USE_CUDA
    using BPCudaType = rtk::CudaBackProjectionImageFilter<MaskImgType>;
    if(!strcmp(args_info.hardware_arg, "cuda") )
      bp = BPCudaType::New();
#endif
    bp->SetInput(zeroVol->GetOutput());
    bp->SetInput(1, ones->GetOutput());
    bp->SetGeometry(geometryReader->GetOutputObject());

    using ThreshType = itk::ThresholdImageFilter<MaskImgType>;
    ThreshType::Pointer thresh = ThreshType::New();
    thresh->SetInput( bp->GetOutput() );
    thresh->ThresholdBelow( geometryReader->GetOutputObject()->GetGantryAngles().size()-1 );
    thresh->SetOutsideValue(0.);

    if(args_info.mask_flag)
      {
      using DivideType = itk::DivideImageFilter<MaskImgType, MaskImgType,  MaskImgType>;
      DivideType::Pointer div = DivideType::New();
      div->SetInput( thresh->GetOutput() );
      div->SetConstant2( geometryReader->GetOutputObject()->GetGantryAngles().size() );

      using WriterType = itk::ImageFileWriter<  MaskImgType >;
      WriterType::Pointer writer = WriterType::New();
      writer->SetFileName( args_info.output_arg );
      writer->SetInput( div->GetOutput() );
      TRY_AND_EXIT_ON_ITK_EXCEPTION( writer->Update() )
      }
    else
      {
      std::cerr << "Option --bp without --mask is not implemented (yet)." << std::endl;
      return EXIT_FAILURE;
      }
    }

  return EXIT_SUCCESS;
}
